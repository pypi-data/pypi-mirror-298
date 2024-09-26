import copy
import importlib
import importlib.abc
import importlib.util
import json
import logging
import os
import pathlib
import subprocess
import sys
import tempfile
import typing

from irisml.core import JobDescription, PatchDescription
import irisml.compiler.stubs


logger = logging.getLogger(__name__)


class Compiler:
    def compile(self, input_filepath, include_paths, build_args: typing.Dict[str, str]):
        include_paths = [str(pathlib.Path(p).resolve()) for p in include_paths]
        env = copy.deepcopy(os.environ)
        env['PYTHONPATH'] = ':'.join(include_paths) + ':' + env.get('PYTHONPATH', '')

        with tempfile.TemporaryDirectory() as tempdir:
            temp_filepath = pathlib.Path(tempdir) / 'tmpfile'
            script_body = f"""
import irisml.compiler
irisml.compiler.compiler.init()
from {input_filepath.stem} import main
irisml.compiler.compiler.generate(main, {repr(str(temp_filepath))}, {repr(build_args)})
"""

            p = subprocess.run([sys.executable, '-c', script_body], capture_output=True, cwd=input_filepath.parent, env=env)
            stderr_str = p.stderr.decode()
            stdout_str = p.stdout.decode()

            if stdout_str:
                print(stdout_str)

            for s in stderr_str.splitlines():
                logger.warning(s)

            if p.returncode != 0:
                raise RuntimeError("Failed to compile.")

            json_str = temp_filepath.read_text()

            try:
                job_description_dict = json.loads(json_str)
            except json.JSONDecodeError:
                raise RuntimeError(f"Failed to parse JSON: {stdout_str}")

            if 'patches' in job_description_dict or 'patches_on_error' in job_description_dict:
                return PatchDescription.from_dict(job_description_dict)

            return JobDescription.from_dict(job_description_dict)


class CompilerSession:
    def __init__(self):
        self._tasks = []
        self._names = set()
        self._on_error = None
        self._patches = []
        self._patches_on_error = []

    def get_unique_name(self, task_name, name):
        """Get a unique name for the task."""
        if name:
            if name in self._names:
                raise ValueError(f'Name {name} is already used.')
            self._names.add(name)
            return name

        if task_name not in self._names:
            self._names.add(task_name)
            return task_name

        i = 1
        while True:
            name = f'{task_name}_{i}'
            if name not in self._names:
                self._names.add(name)
                return name
            i += 1

    def add_task(self, task_instance, task_name, name, inputs, config):
        implicit_name = self.get_unique_name(task_name, name)
        task = {'task': task_name, 'explicit_name': name, 'implicit_name': implicit_name, 'inputs': self._resolve_variable(inputs), 'config': self._resolve_variable(config),
                'task_instance': task_instance}
        self._tasks.append(task)
        return implicit_name

    def get_task(self, task_name, name, inputs, config):
        for task in self._tasks:
            if task['task'] == task_name and task['explicit_name'] == name and task['inputs'] == inputs and task['config'] == config:
                return task
        return None

    def set_on_error(self, tasks):
        self._on_error = [t.to_dict() for t in tasks]

    def add_patch(self, patch: PatchDescription, on_error):
        if on_error:
            self._patches_on_error.append(patch)
        else:
            self._patches.append(patch)

    def generate(self):
        if self._tasks and (self._patches or self._patches_on_error):
            raise ValueError("Tasks and on_error cannot be set at the same time.")

        if self._patches or self._patches_on_error:
            return self._generate_patch()

        def process_task(task):
            t = {'task': task['task'], 'inputs': task['inputs'], 'config': task['config']}
            if task['explicit_name']:
                t['name'] = task['explicit_name']
            elif task['task_instance'].ref_count > 0 and task['implicit_name'] != task['task']:
                t['name'] = task['implicit_name']
            return t

        return JobDescription.from_dict({'tasks': [process_task(t) for t in self._tasks], 'on_error': self._on_error})

    def _generate_patch(self):
        patch = {'patches': [p.to_dict() for p in self._patches],
                 'patches_on_error': [p.to_dict() for p in self._patches_on_error]}

        return PatchDescription.from_dict(patch)

    @staticmethod
    def _resolve_variable(data):
        if isinstance(data, irisml.compiler.stubs.VariableStub):
            return data.resolve()
        if isinstance(data, dict):
            return {k: CompilerSession._resolve_variable(v) for k, v in data.items()}
        if isinstance(data, list):
            return [CompilerSession._resolve_variable(v) for v in data]
        if isinstance(data, irisml.compiler.stubs.OutputsStub):
            raise TypeError(f"OutputsStub is not allowed in the inputs/config: {data}")
        return data


class StubImporter(importlib.abc.MetaPathFinder, importlib.abc.Loader):
    def __init__(self):
        self._enabled = True

    def find_spec(self, fullname, path, target=None):
        if fullname == 'irisml.tasks' and self._enabled:
            # Replace the tasks module with a stub only once.
            self._enabled = False
            self._original_tasks = None
            return importlib.util.spec_from_loader(fullname, self)
        return None

    def create_module(self, spec):
        return irisml.compiler.stubs.TasksModuleStub(spec.name)

    def exec_module(self, module):
        pass  # Do nothing


def init():
    """Initialize the environment for compiler."""
    sys.meta_path.insert(0, StubImporter())


def generate(main, output_filename, build_args):
    """Generate a job description from a main function."""
    session = CompilerSession()
    irisml.compiler.stubs.current_session.set(session)
    main(**build_args)
    irisml.compiler.stubs.current_session.set(None)

    job_description_dict = session.generate().to_dict()

    pathlib.Path(output_filename).write_text(json.dumps(job_description_dict, indent=4))
