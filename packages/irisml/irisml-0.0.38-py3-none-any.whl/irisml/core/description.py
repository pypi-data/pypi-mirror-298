import dataclasses
import typing


def to_dict(x):
    if hasattr(x, 'to_dict'):
        return x.to_dict()
    if isinstance(x, dict):
        return {k: to_dict(v) for k, v in x.items()}
    if isinstance(x, list):
        return [to_dict(v) for v in x]
    return x


@dataclasses.dataclass
class TaskDescription:
    task: str
    name: str | None = None  # Optional name for the task. Must be unique in the job. This name will be used for OutputVariable names.
    inputs: dict[str, typing.Any] = dataclasses.field(default_factory=dict)
    config: dict[str, typing.Any] = dataclasses.field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

    def to_dict(self) -> dict:
        d = {'task': self.task}
        if self.name:
            d['name'] = self.name
        if self.inputs:
            d['inputs'] = to_dict(self.inputs)
        if self.config:
            d['config'] = to_dict(self.config)
        return d


@dataclasses.dataclass
class JobDescription:
    tasks: list[TaskDescription]
    on_error: list[TaskDescription] | None

    @classmethod
    def from_dict(cls, data: dict):
        c = {'tasks': [TaskDescription.from_dict(t) for t in data['tasks']],
             'on_error': data.get('on_error', None) and [TaskDescription.from_dict(t) for t in data['on_error']]}
        return cls(**c)

    def to_dict(self) -> dict:
        d = {'tasks': [t.to_dict() for t in self.tasks]}
        if self.on_error:
            d['on_error'] = [t.to_dict() for t in self.on_error]
        return d


@dataclasses.dataclass
class MatchCondition:
    task: str | None
    name: str | None
    config: dict | None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(task=data.get('task'), name=data.get('name'), config=data.get('config'))

    def to_dict(self) -> dict:
        d = {}
        if self.task:
            d['task'] = self.task
        if self.name:
            d['name'] = self.name
        if self.config:
            d['config'] = self.config
        return d


@dataclasses.dataclass
class SinglePatchDescription:
    match: list[MatchCondition]
    match_if_exists: list[MatchCondition]
    match_oneof: list[MatchCondition]
    top: bool
    bottom: bool

    insert: list[TaskDescription]
    remove: bool
    replace: tuple[list[TaskDescription], dict[str, str]] | None
    update: dict[str, typing.Any] | None

    @classmethod
    def from_dict(cls, data: dict):
        c = {'match': [MatchCondition.from_dict(d) for d in data.get('match', [])],
             'match_if_exists': [MatchCondition.from_dict(d) for d in data.get('match_if_exists', [])],
             'match_oneof': [[MatchCondition.from_dict(d) for d in x] for x in data.get('match_oneof', [])],
             'top': data.get('top', False),
             'bottom': data.get('bottom', False),
             'insert': [TaskDescription.from_dict(t) for t in data.get('insert', [])],
             'remove': data.get('remove', False),
             'replace': None if 'replace' not in data else ([TaskDescription.from_dict(t) for t in data['replace'][0]], data['replace'][1]),
             'update': data.get('update')}
        return cls(**c)

    def to_dict(self) -> dict:
        d = {}
        if self.match:
            d['match'] = [m.to_dict() for m in self.match]
        if self.match_if_exists:
            d['match_if_exists'] = [m.to_dict() for m in self.match_if_exists]
        if self.match_oneof:
            d['match_oneof'] = [[m.to_dict() for m in x] for x in self.match_oneof]
        if self.top:
            d['top'] = True
        if self.bottom:
            d['bottom'] = True
        if self.insert:
            d['insert'] = [t.to_dict() for t in self.insert]
        if self.remove:
            d['remove'] = True
        if self.replace:
            d['replace'] = self.replace and ([t.to_dict() for t in self.replace[0]], self.replace[1])
        if self.update:
            d['update'] = self.update
        return d

    def __post_init__(self):
        num_filters = sum([bool(self.match), bool(self.match_if_exists), bool(self.match_oneof), self.top, self.bottom])
        if num_filters != 1:
            raise ValueError("Exactly one of match, match_if_exists, match_oneof, top, or bottom must be set")

        num_actions = sum([bool(self.insert), self.remove, bool(self.replace), bool(self.update)])
        if num_actions != 1:
            raise ValueError("Exactly one of insert, remove, replace, or update must be set")

        if self.bottom and (self.remove or self.update or self.replace):
            raise ValueError("bottom filter cannot be used with remove, update, or replace actions")


@dataclasses.dataclass
class PatchDescription:
    patches: list[SinglePatchDescription]
    patches_on_error: list[SinglePatchDescription]

    @classmethod
    def from_dict(cls, data: dict):
        c = {'patches': [SinglePatchDescription.from_dict(p) for p in data.get('patches', [])],
             'patches_on_error': [SinglePatchDescription.from_dict(p) for p in data.get('patches_on_error', [])]}
        return cls(**c)

    def to_dict(self) -> dict:
        d = {}
        if self.patches:
            d['patches'] = [p.to_dict() for p in self.patches]
        if self.patches_on_error:
            d['patches_on_error'] = [p.to_dict() for p in self.patches_on_error]
        return d
