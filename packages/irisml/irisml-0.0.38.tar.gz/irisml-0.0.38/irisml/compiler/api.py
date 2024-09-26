import contextlib
import typing

from irisml.compiler.compiler import CompilerSession
from irisml.compiler.stubs import EnvStub, current_session, VariableStub
from irisml.core import SinglePatchDescription


def get_env(name: str):
    return EnvStub(name)


def make_tasks(func: typing.Callable, **kwargs):
    session = CompilerSession()
    with _with_new_session(session):
        func(**kwargs)

    job_description = session.generate()
    return [t.to_dict() for t in job_description.tasks]


def on_error(func: typing.Callable):
    session = CompilerSession()
    with _with_new_session(session):
        func()

    job_description = session.generate()
    if not job_description.tasks:
        raise RuntimeError("on_error must have at least one task")

    current_session.get().set_on_error(job_description.tasks)


def make_patch(match: typing.Callable | None = None,
               match_if_exists: typing.Callable | None = None,
               match_oneof: typing.Callable | None = None,
               top: bool = False,
               bottom: bool = False,
               insert: typing.Callable | None = None,
               remove: bool = False,
               replace: tuple[typing.Callable, dict[str, str]] | None = None,
               update: dict | None = None,
               on_error: bool = False):
    if sum(1 for a in (match, match_if_exists, match_oneof, top, bottom) if a) != 1:
        raise ValueError("Exactly one of match, match_if_exists, match_oneof, top, or bottom must be set")
    if sum(1 for a in (insert, remove, replace, update) if a) != 1:
        raise ValueError("Exactly one of insert, remove, replace, or update must be set")

    patch_dict = {}
    if match:
        patch_dict['match'] = _get_match_condition(match)
    elif match_if_exists:
        patch_dict['match_if_exists'] = _get_match_condition(match_if_exists)
    elif match_oneof:
        patch_dict['match_oneof'] = [_get_match_condition(m) for m in match_oneof]
    elif top:
        patch_dict['top'] = True
    elif bottom:
        patch_dict['bottom'] = True

    if insert:
        patch_dict['insert'] = make_tasks(insert)
    elif remove:
        patch_dict['remove'] = True
    elif replace:
        patch_dict['replace'] = (make_tasks(replace[0]), replace[1])
    elif update:
        patch_dict['update'] = _resolve_stub(update)

    current_session.get().add_patch(SinglePatchDescription.from_dict(patch_dict), on_error)


def _resolve_stub(stub):
    if isinstance(stub, VariableStub):
        return stub.resolve()
    elif isinstance(stub, dict):
        return {k: _resolve_stub(v) for k, v in stub.items()}
    elif isinstance(stub, list):
        return [_resolve_stub(v) for v in stub]
    return stub


def _get_match_condition(match):
    if not isinstance(match, typing.Callable):
        raise ValueError("Match Condition must be a callable")

    session = CompilerSession()
    with _with_new_session(session):
        match()

    job_description = session.generate()
    job_dict = job_description.to_dict()
    return job_dict['tasks']


@contextlib.contextmanager
def _with_new_session(session):
    old_session = current_session.get()
    current_session.set(session)
    yield
    current_session.set(old_session)
