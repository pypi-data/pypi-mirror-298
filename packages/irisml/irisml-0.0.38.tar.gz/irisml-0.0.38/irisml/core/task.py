import dataclasses
import importlib
import logging
import random
import time
import types
import typing
from irisml.core import TaskDescription
from .hash_generator import HashGenerator
from .task_base import TaskBase
from .variable import replace_variables, Variable


logger = logging.getLogger(__name__)


class Task:
    """Represents a task. It doesn't require actual task modules until load_module() is called."""
    def __init__(self, description: TaskDescription):
        assert description.task.islower()

        self._task_name = description.task
        self._inputs_dict = replace_variables(description.inputs or {})
        self._config_dict = replace_variables(description.config or {})
        self._name = description.name or self._task_name
        self._task_class = None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def task_name(self):
        return self._task_name

    def execute(self, context, dry_run=False):
        if dry_run:
            return self.dry_run(context)

        if not self._task_class:
            raise RuntimeError("load_module() must be called before executing the task.")

        config = self._load_config(self._task_class.Config, self._config_dict)
        inputs = self._load_inputs(self._task_class.Inputs, self._inputs_dict)

        if context.is_cache_enabled and self._task_class.CACHE_ENABLED:
            task_hash = HashGenerator.calculate_hash([config, inputs], context)
            cached_outputs = context.get_cached_outputs(self._task_name, self._task_class.VERSION, task_hash, self._task_class.Outputs)
            context.add_execution_log(self.name, self.task_name, self._task_class.VERSION, task_hash, config, inputs, cache_hit=bool(cached_outputs))
            if cached_outputs:
                logger.info(f"[{self._task_name}]: Found cached outputs. Skipping the task.")
                context.add_outputs(self.name, cached_outputs)
                return cached_outputs
        else:
            context.add_execution_log(self.name, self.task_name, self._task_class.VERSION, None, config, inputs, cache_hit=False)

        logger.info(f"[{self._task_name}] Started. Version={self._task_class.VERSION}")
        start_time = time.time()
        # If RESOLVE_CONFIG_VARIABLES is False, the task will be responsible for resolving the configs.
        assert self._task_class.RESOLVE_CONFIG_VARIABLES or not self._task_class.CACHE_ENABLED
        resolved_config = context.resolve(config) if self._task_class.RESOLVE_CONFIG_VARIABLES else config
        resolved_inputs = context.resolve(inputs)

        if self._task_class.CACHE_ENABLED and context.is_cache_enabled:
            if HashGenerator.calculate_hash(config, context) != HashGenerator.calculate_hash(resolved_config):
                logger.error("Resolved config has different hash.")
            if HashGenerator.calculate_hash(inputs, context) != HashGenerator.calculate_hash(resolved_inputs):
                logger.error("Resolved inputs has different hash.")

        self._reset_random_seed()
        logger.debug(f"Instantiating the task module. config={resolved_config}")
        task = self._task_class(resolved_config, context)
        outputs = task.execute(resolved_inputs)
        if outputs is None:
            raise RuntimeError(f"The task {self._task_name} returned None.")
        if not isinstance(outputs, self._task_class.Outputs):
            raise RuntimeError(f"Task {self._task_name} returned invalid outputs: {outputs}")

        logger.info(f"[{self._task_name}] Completed. {time.time() - start_time:.3f}s")

        context.add_outputs(self.name, outputs)
        if self._task_class.CACHE_ENABLED and context.is_cache_enabled:
            context.add_cache_outputs(self._task_name, self._task_class.VERSION, task_hash, outputs)

        self._release_cache()
        return outputs

    def dry_run(self, context):
        """Dry run the task. Task can define its own dry_run() method."""
        if not self._task_class:
            raise RuntimeError("load_module() must be called before executing the task.")

        config = self._load_config(self._task_class.Config, self._config_dict)
        inputs = self._load_inputs(self._task_class.Inputs, self._inputs_dict)

        assert self._task_class.RESOLVE_CONFIG_VARIABLES or not self._task_class.CACHE_ENABLED
        resolved_config = context.resolve(config) if self._task_class.RESOLVE_CONFIG_VARIABLES else config
        resolved_inputs = context.resolve(inputs)

        logger.debug(f"Instantiating the task module. config={resolved_config}")
        task = self._task_class(resolved_config, context)
        outputs = task.dry_run(resolved_inputs)

        if not isinstance(outputs, self._task_class.Outputs):
            raise RuntimeError(f"Task {self._task_name} returned invalid outputs: {outputs}")

        context.add_outputs(self.name, outputs)
        return outputs

    def load_module(self):
        """Load a task module dynamically. If the module was not found, throws a RuntimeError"""
        task_module_name = 'irisml.tasks.' + self.task_name
        try:
            task_module = importlib.import_module(task_module_name)
        except ModuleNotFoundError as e:
            if e.name == task_module_name:
                raise RuntimeError(f"Task not found: {task_module_name}") from e
            else:
                raise

        task_class = getattr(task_module, 'Task')
        if not issubclass(task_class, TaskBase):
            raise RuntimeError(f"Failed to load {self.task_name}. Please make sure the Task class inherits the TaskBase class.")
        self._task_class = task_class

        # Verify that the config is loadable.
        self._load_config(task_class.Config, self._config_dict)
        self.validate()

    def validate(self):
        """Check if the task satisfies the rules."""
        if not self._task_class:
            raise RuntimeError("load_module() must be called first.")

        if self._task_class.VERSION == '0.0.0':
            logger.warning(f"Task {self._task_name} is version 0.0.0. Please define VERSION attribute in the Task class..")

        if not dataclasses.is_dataclass(self._task_class.Config):
            raise RuntimeError(f"Config class must be a dataclass. Actual: {type(self._task_class.Config)}")
        if not dataclasses.is_dataclass(self._task_class.Inputs):
            raise RuntimeError(f"Inputs class must be a dataclass. Actual: {type(self._task_class.Inputs)}")
        if not dataclasses.is_dataclass(self._task_class.Outputs):
            raise RuntimeError(f"Outputs class must be a dataclass. Actual: {type(self._task_class.Outputs)}")

        for f in dataclasses.fields(self._task_class.Inputs):
            if dataclasses.is_dataclass(f.type):
                raise RuntimeError(f"Nested input dataclass is not allowed: {f.name}")

        for f in dataclasses.fields(self._task_class.Outputs):
            if dataclasses.is_dataclass(f.type):
                raise RuntimeError(f"Nested output dataclass is not allowed: {f.name}")

    @staticmethod
    def _load_config(config_class, config_dict):  # noqa: C901 # TODO
        """Initialize a config class loaded from the actual task module."""
        assert dataclasses.is_dataclass(config_class)

        def load(type_class, value):
            origin = typing.get_origin(type_class)
            args = typing.get_args(type_class)
            if dataclasses.is_dataclass(type_class):
                assert isinstance(value, dict)
                c = {}
                for field in dataclasses.fields(type_class):
                    if field.name in value:
                        c[field.name] = load(field.type, value[field.name])

                unused_keys = set(value.keys()) - set(c.keys())
                if unused_keys:
                    raise ValueError(f"There are redundant fields: {unused_keys}")
                return type_class(**c)
            elif origin is tuple:
                return tuple(load(arg, v) for arg, v in zip(args, value))
            elif origin is list:
                if isinstance(value, Variable):
                    value.expected_type = list
                    return value
                return [load(args[0], v) for v in value]
            elif origin is dict:
                if isinstance(value, Variable):
                    value.expected_type = dict
                    return value
                return {load(args[0], k): load(args[1], v) for k, v in value.items()}
            elif origin in (typing.Union, types.UnionType):  # Optional[X] is Union[X, NoneType]
                if len(args) == 2 and type(None) in args:
                    expected_type = next(a for a in args if a is not type(None))  # noqa: E721
                    return load(expected_type, value) if value is not None else None
                elif type(value) in args:
                    return value
                else:
                    raise ValueError(f"Union type is not allowed: {type_class}")
            elif type_class == typing.Any:
                return value
            elif origin is None:
                if isinstance(value, Variable):
                    value.expected_type = type_class
                    return value
                return type_class(value)
            elif origin is typing.Literal:
                if isinstance(value, Variable):
                    value.expected_type = type_class
                elif value and value not in args:
                    raise ValueError(f"Unexpected literal value: {value}. Expected: {args}")
                return value
            else:
                raise ValueError(f"Config data type is not supported: {type_class} value: {value}")

        return load(config_class, config_dict)

    @staticmethod
    def _load_inputs(inputs_class, inputs_dict: dict):
        c = {}
        # Inputs doesn't have nested values.
        for field in dataclasses.fields(inputs_class):
            if field.name in inputs_dict:
                if isinstance(inputs_dict[field.name], Variable):
                    inputs_dict[field.name].expected_type = field.type
                c[field.name] = inputs_dict[field.name]
        return inputs_class(**c)

    def _reset_random_seed(self):
        """Reset the random seed.

        To make sure the tasks are deterministic, we reset the random seed every time a task starts.
        """
        # import torch lazily to avoid slowing down the startup time.
        import torch
        torch.manual_seed(42)
        random.seed(42)

    def _release_cache(self):
        # import torch lazily
        import torch
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

    def __str__(self):
        return f"Task {self.task_name} (name: {self.name})"
