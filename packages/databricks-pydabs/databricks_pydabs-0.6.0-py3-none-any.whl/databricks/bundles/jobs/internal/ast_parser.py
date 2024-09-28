import ast
import inspect
import os
import re
import textwrap
from dataclasses import dataclass, replace
from enum import Enum
from types import MethodType
from typing import Any, Callable, Optional

from databricks.bundles.jobs.functions.compute import ComputeTask
from databricks.bundles.jobs.functions.sql_file_task import SqlFileTaskWithOutput
from databricks.bundles.jobs.functions.sql_query_task import SqlQueryTaskWithOutput
from databricks.bundles.jobs.functions.task import TaskFunction, TaskWithOutput
from databricks.bundles.jobs.functions.task_parameter import (
    ConstantParameter,
    ForEachInputTaskParameter,
    JobParameter,
    TaskParameter,
    TaskReferenceParameter,
    VariableParameter,
)
from databricks.bundles.jobs.internal.parameters import _serialize_parameter
from databricks.bundles.jobs.models.task import Task, TaskDependency
from databricks.bundles.jobs.models.tasks.condition_task import (
    ConditionTask,
    ConditionTaskOp,
)
from databricks.bundles.jobs.models.tasks.for_each_task import ForEachTask
from databricks.bundles.variables import Variable, VariableOr, resolve_variable

TASK_KEY_REGEX = r"^[a-zA-Z0-9\-_]+$"

# constants used for task_key generation
MAX_TASK_KEY_LENGTH = 100

NodeType = ast.stmt | ast.expr


class InternalJobError(Exception):
    node: NodeType

    def __init__(self, node: NodeType, message: str, use_end_col: bool = False) -> None:
        assert isinstance(node, NodeType)
        self.node = node
        self.message = message
        self.use_end_col = use_end_col  # if true, point error to the end of 'node'


@dataclass
class ParsedJob:
    tasks: list[Task]
    parameters: dict[str, JobParameter]


@dataclass(frozen=True)
class Value:
    expr: ast.expr
    unboxed: Any
    name: Optional[str] = None


@dataclass
class Scope:
    closure_vars: dict
    nonlocals: dict
    tasks: dict[str, Task]
    local_vars: dict
    condition: Optional[TaskDependency]
    file: Optional[str]
    start_line_no: Optional[int]
    source_lines: list[str]


@dataclass
class TaskValuesImpl:
    task_key: str


@dataclass
class TaskOutputImpl:
    task_key: str


def _require_primitive_value(arg_value: Value):
    if isinstance(arg_value.unboxed, Task):
        raise InternalJobError(arg_value.expr, "Can't reference tasks in this context")

    if isinstance(arg_value.unboxed, TaskParameter):
        raise InternalJobError(
            arg_value.expr, "Can't reference parameters in this context"
        )

    if isinstance(arg_value.unboxed, TaskValuesImpl):
        raise InternalJobError(
            arg_value.expr, "Can't reference task values in this context"
        )

    if isinstance(arg_value.unboxed, TaskOutputImpl):
        raise InternalJobError(
            arg_value.expr, "Can't reference task outputs in this context"
        )


def _eval_expr(expr: ast.expr, scope: Scope) -> Value:
    value = _eval_expr_unchecked(expr, scope)

    _require_primitive_value(value)

    return value


def _eval_task_result(
    task: TaskWithOutput, expr: ast.Attribute
) -> TaskReferenceParameter:
    if isinstance(task, ComputeTask):
        return TaskReferenceParameter(
            task_key=resolve_variable(task.task_key),
            path=["values", "return_value"],
        )

    if isinstance(task, SqlQueryTaskWithOutput):
        return TaskReferenceParameter(
            task_key=resolve_variable(task.task_key),
            path=["output", "rows"],
        )

    if isinstance(task, SqlFileTaskWithOutput):
        return TaskReferenceParameter(
            task_key=resolve_variable(task.task_key),
            path=["output", "rows"],
        )

    raise InternalJobError(expr, "Task doesn't have a result")


def _eval_attribute(expr: ast.Attribute, scope: Scope) -> Value:
    # special case to allow parameter referencing
    lhs_value = _eval_expr_unchecked(expr.value, scope)
    lhs = lhs_value.unboxed

    if not isinstance(expr.ctx, ast.Load):
        raise InternalJobError(expr, "Unsupported expression")

    if isinstance(lhs, TaskWithOutput) and expr.attr == "result":
        if not lhs_value.name:
            raise InternalJobError(
                expr,
                "Task has to be assigned to a variable before it can be referenced",
            )

        if not lhs.task_key:
            raise InternalJobError(
                expr, "Can't reference task because 'task_key' isn't set"
            )

        return Value(expr, _eval_task_result(lhs, expr))

    if isinstance(lhs, TaskReferenceParameter) and lhs.path == [
        "output",
        "first_row",
    ]:
        parameter = TaskReferenceParameter(
            task_key=resolve_variable(lhs.task_key),
            path=[*lhs.path, expr.attr],
        )

        return Value(expr, parameter)

    if isinstance(lhs, TaskWithOutput) and expr.attr == "output":
        if lhs.task_key is None:
            raise InternalJobError(
                expr, "Can't reference task because 'task_key' isn't set"
            )

        return Value(
            expr,
            TaskOutputImpl(task_key=resolve_variable(lhs.task_key)),
        )

    if isinstance(lhs, TaskOutputImpl):
        return Value(
            expr,
            TaskReferenceParameter(
                task_key=resolve_variable(lhs.task_key),
                path=["output", expr.attr],
            ),
        )

    if isinstance(lhs, ComputeTask) and expr.attr == "values":
        if lhs.task_key is None:
            raise InternalJobError(
                expr, "Can't reference task because 'task_key' isn't set"
            )

        return Value(
            expr,
            TaskValuesImpl(resolve_variable(lhs.task_key)),
        )

    if isinstance(lhs, TaskValuesImpl):
        return Value(
            expr,
            TaskReferenceParameter(
                task_key=resolve_variable(lhs.task_key),
                path=["values", expr.attr],
            ),
        )

    if isinstance(lhs, ForEachInputTaskParameter):
        if lhs.attribute is not None:
            raise InternalJobError(
                expr, "Accessing attributes deeper than one level isn't supported"
            )

        return Value(
            expr,
            ForEachInputTaskParameter(attribute=expr.attr),
        )

    if isinstance(lhs, TaskReferenceParameter) or isinstance(lhs, JobParameter):
        raise InternalJobError(
            expr.value,
            "Accessing attributes of task values, job parameters or task outputs is not supported",
            use_end_col=True,
        )

    # TODO, here we can support referencing other parameter types, e.g. run_id

    return Value(expr, getattr(lhs, expr.attr))


def _eval_expr_unchecked(expr: ast.expr, scope: Scope) -> Value:
    if isinstance(expr, ast.Call):
        return _eval_call(expr, scope)
    elif isinstance(expr, ast.Constant):
        return Value(expr, expr.value)
    elif isinstance(expr, ast.List):
        unboxed = [_eval_expr(elt, scope).unboxed for elt in expr.elts]

        return Value(expr, unboxed)
    elif isinstance(expr, ast.Attribute):
        return _eval_attribute(expr, scope)
    elif isinstance(expr, ast.Name):
        if expr.id in scope.local_vars:
            return Value(expr, scope.local_vars[expr.id], name=expr.id)

        if expr.id in scope.closure_vars or expr.id in scope.nonlocals:
            unboxed = scope.closure_vars.get(expr.id) or scope.nonlocals[expr.id]

            if isinstance(unboxed, Task):
                raise InternalJobError(
                    expr, "Referencing tasks from closure isn't supported"
                )

            return Value(expr, unboxed, name=expr.id)

        raise InternalJobError(expr, f"Name '{expr.id}' is not defined")
    elif isinstance(expr, ast.JoinedStr):
        return _eval_joined_str(expr, scope)
    else:
        raise InternalJobError(expr, "Unsupported expression")


def _eval_formatted_value(expr: ast.FormattedValue, scope: Scope) -> str:
    # from docs:
    # -1: no formatting
    # 115: !s string formatting
    # 114: !r repr formatting
    # 97: !a ascii formatting

    if expr.conversion == -1:
        arg = _eval_expr(expr.value, scope).unboxed
    elif expr.conversion == 115:
        arg = str(_eval_expr(expr.value, scope).unboxed)
    elif expr.conversion == 114:
        arg = repr(_eval_expr(expr.value, scope).unboxed)
    elif expr.conversion == 97:
        arg = ascii(_eval_expr(expr.value, scope).unboxed)
    else:
        raise InternalJobError(expr, "Unsupported expression")

    if expr.format_spec:
        assert isinstance(expr.format_spec, ast.JoinedStr)

        format_spec = _eval_joined_str(expr.format_spec, scope).unboxed
        return arg.__format__(format_spec)
    else:
        return "{}".format(arg)


def _eval_joined_str(expr: ast.JoinedStr, scope: Scope) -> Value:
    unboxed = ""

    for value in expr.values:
        if isinstance(value, ast.FormattedValue):
            unboxed += _eval_formatted_value(value, scope)
        elif isinstance(value, ast.Constant):
            assert isinstance(value.value, str)

            unboxed += value.value
        else:
            raise InternalJobError(expr, "Unsupported expression")

    return Value(expr, unboxed)


def _check_func_arg(func_value: Value, arg_value: Value):
    func = func_value.unboxed
    arg = arg_value.unboxed

    if isinstance(arg, TaskParameter):
        if isinstance(func, TaskFunction):
            pass
        else:
            raise InternalJobError(
                arg_value.expr,
                "Can't pass job parameters or task outputs into non-task "
                "functions. Did you forget @task annotation?",
            )

    if isinstance(arg, Task):
        # tasks are ok to pass as arguments, e.g. add_depends_on
        if isinstance(func, MethodType) and isinstance(func.__self__, Task):
            pass
        else:
            raise InternalJobError(
                arg_value.expr, "Can't reference tasks in this context"
            )


def _eval_call(call: ast.Call, scope: Scope) -> Value:
    args = []
    kwargs = {}

    func_value = _eval_expr_unchecked(call.func, scope)
    func = func_value.unboxed

    for arg in call.args:
        arg_value = _eval_expr_unchecked(arg, scope)
        arg = arg_value.unboxed

        args.append(arg)

        _check_func_arg(func_value, arg_value)

    for keyword in call.keywords:
        arg_value = _eval_expr_unchecked(keyword.value, scope)
        arg = arg_value.unboxed

        kwargs[keyword.arg] = arg

        _check_func_arg(func_value, arg_value)

    if isinstance(func, TaskParameter):
        raise InternalJobError(
            call.func,
            "Calling methods on task parameters is not supported",
            use_end_col=True,
        )
    elif isinstance(func, TaskValuesImpl):
        raise InternalJobError(
            call.func, "Task values object is not callable", use_end_col=True
        )
    elif variable := _unwrap_variable_get(func):
        unboxed = VariableParameter(variable=variable)

        return Value(call, unboxed)
    else:
        # this is a catch-all, we should generate more contextual error
        # messages above if possible
        _require_primitive_value(func_value)

    # we assume that 'func' is callable, if not, let it crash
    unboxed = func.__call__(*args, **kwargs)  # type: ignore

    return Value(call, unboxed)


def _unwrap_variable_get(func) -> Optional[Variable]:
    if not inspect.ismethod(func):
        return None

    if func.__func__ != Variable.get:
        return None

    self = func.__self__
    assert isinstance(self, Variable)

    return self


def eval_job_func(job_function: Callable, scope: Scope) -> list[Task]:
    source = inspect.getsource(job_function)
    source = textwrap.dedent(source)
    module: ast.Module = ast.parse(source)

    scope.source_lines = source.splitlines()

    scope.start_line_no = start_line_no = inspect.findsource(job_function)[1]
    scope.file = file = scope.file or os.path.relpath(inspect.getfile(job_function))

    body_statement = _single_stmt(module.body)
    function_def = _parse_function_def(body_statement)

    try:
        _eval_function_def(function_def, scope)

        if len(scope.tasks) == 0:
            raise InternalJobError(body_statement, "Job must have at least one task")

        return list(scope.tasks.values())
    except InternalJobError as e:
        error = _map_to_syntax_error(
            e,
            start_line_no=start_line_no,
            file=file,
            source=source,
        )

        raise error from None


def _map_to_syntax_error(
    e: InternalJobError,
    source: str,
    start_line_no: int,
    file: str,
) -> SyntaxError:
    # avoid cyclic imports, we want to keep JobSyntaxError
    # in databricks.workflows to have short qualified name
    from databricks.bundles.jobs import JobSyntaxError

    error_line_no = start_line_no + e.node.lineno

    all_lines = source.splitlines(keepends=True)
    relevant_lines = all_lines[e.node.lineno - 1 : e.node.lineno]

    col_offset = e.node.col_offset
    if e.use_end_col:
        col_offset = e.node.end_col_offset or col_offset

    return JobSyntaxError(
        e.message,
        (file, error_line_no, col_offset + 1, next(iter(relevant_lines), "")),
    )


def _get_expr_source_lines(expr: ast.expr, source_lines: list[str]) -> list[str]:
    """
    Get source for arbitrary expression.
    """
    lines = list[str]()

    end_lineno = expr.end_lineno or expr.lineno

    if expr.lineno == end_lineno:
        if len(source_lines) >= expr.lineno:
            line = source_lines[expr.lineno - 1]
            line = line[expr.col_offset : expr.end_col_offset]

            lines.append(line)
    else:
        if len(source_lines) >= expr.lineno:
            line = source_lines[expr.lineno - 1]
            line = line[expr.col_offset :]

            lines.append(line)

        for i in range(expr.lineno + 1, end_lineno):
            lines.append(source_lines[i - 1])

        if len(source_lines) >= end_lineno:
            line = source_lines[end_lineno - 1]
            line = line[: expr.end_col_offset]

            lines.append(line)

    return lines


def _inject_defaults(stmt: ast.stmt, task: Task, scope: Scope) -> Task:
    if scope.condition:
        depends_on = resolve_variable(task.depends_on)
        task = replace(task, depends_on=[*depends_on, scope.condition])

    return task


def _eval_assign(assign: ast.Assign, scope: Scope):
    name, unboxed = _parse_assign(assign, scope)

    if isinstance(unboxed, Task):
        unboxed = _register_task(assign, unboxed, scope)

    scope.local_vars[name] = unboxed


def _parse_assign(assign: ast.Assign, scope: Scope) -> tuple[str, Any]:
    assert isinstance(assign, ast.Assign)

    name = _parse_name(_single_expr(assign.targets))

    # because we do name aliasing, we allow any type
    unboxed = _eval_expr_unchecked(assign.value, scope).unboxed

    if isinstance(unboxed, Task):
        unboxed = replace(unboxed, task_key=name)

    return name, unboxed


def _eval_stmt(stmt: ast.stmt, scope: Scope):
    if isinstance(stmt, ast.Assign):
        _eval_assign(stmt, scope)
    elif isinstance(stmt, ast.Expr):
        # top-level statements can evaluate to anything unchecked
        value = _eval_expr_unchecked(stmt.value, scope)

        if isinstance(value.unboxed, Task):
            _register_task(stmt, value.unboxed, scope)
    elif isinstance(stmt, ast.If):
        condition_step = _parse_condition_step(stmt.test, scope)
        condition_step = _register_task(stmt, condition_step, scope)

        prev_outcome = scope.condition

        assert condition_step.task_key

        scope.condition = TaskDependency(condition_step.task_key, outcome="true")
        _eval_stmt_list(stmt.body, scope)

        scope.condition = TaskDependency(condition_step.task_key, outcome="false")
        _eval_stmt_list(stmt.orelse, scope)

        scope.condition = prev_outcome
    elif isinstance(stmt, ast.Return):
        pass
    elif isinstance(stmt, ast.For):
        _eval_for_each(stmt, scope)
    else:
        raise InternalJobError(stmt, "Unsupported statement")


def _eval_for_each(stmt: ast.For, scope: Scope):
    if stmt.orelse:
        raise InternalJobError(
            stmt.orelse[0], "Combination 'for' and 'else' isn't supported"
        )

    target = _parse_name(stmt.target)
    iter = _eval_expr_unchecked(stmt.iter, scope).unboxed

    if isinstance(iter, Task):
        raise InternalJobError(
            stmt.iter, "Can't iterate task, did you forget .result or .output?"
        )

    if len(stmt.body) != 1:
        raise InternalJobError(stmt, "Only for loops with a single task are supported")

    [task_stmt] = stmt.body

    iteration_scope = replace(
        scope,
        local_vars={**scope.local_vars, target: ForEachInputTaskParameter()},
    )

    if isinstance(task_stmt, ast.Assign):
        _, iteration_task = _parse_assign(task_stmt, iteration_scope)
    elif isinstance(task_stmt, ast.Expr):
        iteration_task = _eval_expr_unchecked(task_stmt.value, iteration_scope).unboxed
    elif isinstance(task_stmt, ast.For):
        raise InternalJobError(task_stmt, "Nested for loops are not supported")
    elif isinstance(task_stmt, ast.If):
        raise InternalJobError(
            task_stmt,
            "Conditions nested in for loops are not supported",
        )
    else:
        raise InternalJobError(
            task_stmt,
            "Only 'x = my_task(iter)' or 'my_task(iter)' is supported in for loops",
        )

    if not isinstance(iteration_task, Task):
        raise InternalJobError(task_stmt, "Only tasks are supported in for loops")

    if iteration_task.for_each_task:
        raise InternalJobError(task_stmt, "Nested for loops are not supported")
    elif iteration_task.condition_task:
        raise InternalJobError(
            task_stmt,
            "Conditions nested in for loops are not supported",
        )

    assert iteration_task.task_key

    if isinstance(iter, TaskParameter):
        inputs = iter.serialize()
    else:
        # FIXME we need to give a better type hint to 'iter'
        inputs = _serialize_parameter(type(iter), iter)

    if isinstance(iter, TaskReferenceParameter):
        depends_on = [TaskDependency(iter.task_key)]
    else:
        depends_on = []

    task = Task(
        task_key=f"foreach_{target}_{iteration_task.task_key}",
        for_each_task=ForEachTask(
            inputs=inputs,
            task=iteration_task,
        ),
        depends_on=[*depends_on],  # copy to help type inference
    )

    # nested task in cannot have dependencies, so we move them to outer task
    if iteration_task.depends_on:
        assert task.for_each_task

        depends_on = resolve_variable(task.depends_on)
        iteration_task_depends_on = resolve_variable(iteration_task.depends_on)
        for_each_task = resolve_variable(task.for_each_task)
        for_each_task_task = resolve_variable(for_each_task.task)

        task = replace(
            task,
            depends_on=[*depends_on, *iteration_task_depends_on],
            for_each_task=replace(
                for_each_task,
                task=replace(for_each_task_task, depends_on=None),
            ),
        )

    _register_task(stmt, task, scope)


def _eval_stmt_list(stmts: list[ast.stmt], scope: Scope):
    for stmt in stmts:
        _eval_stmt(stmt, scope)


def _register_task(stmt: ast.stmt, task: Task, scope: Scope) -> Task:
    task = _inject_defaults(stmt, task, scope)
    task_key = resolve_variable(task.task_key)

    if not task_key:
        raise InternalJobError(
            stmt,
            "Job tasks must be assigned to a variable or use 'with_task_key'",
        )

    existing = scope.tasks.get(task_key)

    if existing:
        raise InternalJobError(stmt, f"Task with task key '{task_key}' already exists")

    task = replace(task, task_key=task_key)

    _validate_task(stmt, task)

    scope.tasks[task_key] = task

    return task


def _validate_task(stmt: ast.stmt, task: Task):
    if task.environment_key:
        if task.notebook_task:
            raise InternalJobError(
                stmt,
                "Can't set environment_key for notebook tasks, configure "
                "environment on a notebook instead. See https://docs.databricks.com/en/compute/serverless.html",
            )


def _parse_condition_step(expr: ast.expr, scope: Scope) -> Task:
    if isinstance(expr, ast.Compare):
        if len(expr.comparators) != 1 or len(expr.ops) != 1:
            raise InternalJobError(expr, "Unsupported condition")

        # there are no limitations of what can be used in conditional tests
        left_value = _eval_expr_unchecked(expr.left, scope)
        right_value = _eval_expr_unchecked(expr.comparators[0], scope)
        op = _parse_operator(expr.ops[0], parent=expr)
    else:
        raise InternalJobError(expr, "Unsupported condition")

    def wrap_parameter(value: Value) -> TaskParameter:
        if isinstance(value.unboxed, TaskParameter):
            return value.unboxed

        _require_primitive_value(value)

        return ConstantParameter(value.unboxed)

    left_parameter = wrap_parameter(left_value)
    right_parameter = wrap_parameter(right_value)
    left_name = _generate_task_key_part(left_parameter)
    right_name = _generate_task_key_part(right_parameter)
    task_key = f"if_{left_name}_{op.name.lower()}_{right_name}"

    depends_on = list[VariableOr[TaskDependency]]()

    if isinstance(left_parameter, TaskReferenceParameter):
        depends_on.append(TaskDependency(left_parameter.task_key))

    if isinstance(right_parameter, TaskReferenceParameter):
        depends_on.append(TaskDependency(right_parameter.task_key))

    return Task(
        task_key=task_key,
        depends_on=depends_on,
        condition_task=ConditionTask(
            left=left_parameter.serialize(),
            right=right_parameter.serialize(),
            op=op,
        ),
    )


def _generate_task_key_part_for_str(value: str) -> str:
    # there is left and right part + 1/3 reserved for operator
    limit = int(MAX_TASK_KEY_LENGTH / 3)
    fixed_str = value.replace(" ", "_")[0:limit]

    if _valid_task_key(fixed_str):
        return fixed_str

    return "expr"


def _generate_task_key_part(param: TaskParameter):
    if isinstance(param, TaskReferenceParameter):
        return param.task_key
    elif isinstance(param, ConstantParameter):
        if isinstance(param.value, int):
            return str(param.value)
        elif isinstance(param.value, Enum):
            return _generate_task_key_part_for_str(param.value.name)
        elif isinstance(param.value, str):
            return _generate_task_key_part_for_str(param.value)

    return "expr"


def _parse_operator(op: ast.cmpop, parent: NodeType) -> ConditionTaskOp:
    if isinstance(op, ast.Eq):
        return ConditionTaskOp.EQUAL_TO
    elif isinstance(op, ast.NotEq):
        return ConditionTaskOp.NOT_EQUAL
    elif isinstance(op, ast.Gt):
        return ConditionTaskOp.GREATER_THAN
    elif isinstance(op, ast.GtE):
        return ConditionTaskOp.GREATER_THAN_OR_EQUAL
    elif isinstance(op, ast.Lt):
        return ConditionTaskOp.LESS_THAN
    elif isinstance(op, ast.LtE):
        return ConditionTaskOp.LESS_THAN_OR_EQUAL
    else:
        raise InternalJobError(parent, f"Unsupported operator: {op}")


def _eval_function_def(function_def: ast.FunctionDef, scope: Scope):
    _eval_stmt_list(function_def.body, scope)


def _parse_name(expr: ast.expr) -> str:
    if isinstance(expr, ast.Attribute):
        raise InternalJobError(expr, f"Unexpected expression {expr.attr}")

    if not isinstance(expr, ast.Name):
        raise InternalJobError(expr, "Unexpected expression")

    return expr.id


def _parse_function_def(expr: ast.stmt) -> ast.FunctionDef:
    if not isinstance(expr, ast.FunctionDef):
        raise InternalJobError(expr, "Unexpected expression")

    return expr


def _single_expr(exprs: list[ast.expr]) -> ast.expr:
    assert len(exprs) == 1

    return exprs[0]


def _single_stmt(exprs: list[ast.stmt]) -> ast.stmt:
    assert len(exprs) == 1

    return exprs[0]


def _valid_task_key(task_key: str) -> bool:
    return re.match(TASK_KEY_REGEX, task_key) is not None
