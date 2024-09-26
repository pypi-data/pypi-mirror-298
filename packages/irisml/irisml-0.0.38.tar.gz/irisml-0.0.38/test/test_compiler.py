import pathlib
import tempfile
import textwrap
import unittest
from irisml.core import JobDescription, PatchDescription
from irisml.compiler import Compiler


class TestCompiler(unittest.TestCase):
    def test_simple(self):
        input_str = """
        from irisml.tasks import task_a, task_b

        def main():
            output = task_a()
            output = task_b(in_int=output.out_int)
        """
        expected_job_description = JobDescription.from_dict({'tasks': [
            {'task': 'task_a'},
            {'task': 'task_b', 'inputs': {'in_int': '$output.task_a.out_int'}}]})

        self.check_compile(input_str, expected_job_description)

    def test_unique_names(self):
        input_str = """
        from irisml.tasks import task_a, task_b

        def main():
            output = task_a()
            task_a()
            output2 = task_a()
            task_b(in_int=output.out_int)
            task_b(in_int=output2.out_int)
        """
        expected_job_description = JobDescription.from_dict({'tasks': [
            {'task': 'task_a'},
            {'task': 'task_a'},  # Doesn't have an explicit name because the output is not used.
            {'task': 'task_a', 'name': 'task_a_2'},
            {'task': 'task_b', 'inputs': {'in_int': '$output.task_a.out_int'}},
            {'task': 'task_b', 'inputs': {'in_int': '$output.task_a_2.out_int'}}]})
        self.check_compile(input_str, expected_job_description)

    def test_manual_names(self):
        input_str = """
        from irisml.tasks import task_a

        def main():
            task_a(_name='my_dataset')
        """
        expected_job_description = JobDescription.from_dict({'tasks': [{'task': 'task_a', 'name': 'my_dataset'}]})
        self.check_compile(input_str, expected_job_description)

    def test_cached(self):
        input_str = """
        from irisml.tasks import task_b, task_d
        def main():
            task_d()
            task_d()
            a = task_d()
            task_d(in_int=100)
            task_d(in_int=100)
            task_d(in_int=3)
            task_d(_name='my_task')
            task_b(in_int=a.out_int)
        """
        expected_job_description = JobDescription.from_dict({'tasks': [
            {'task': 'task_d'},
            {'task': 'task_d', 'config': {'in_int': 100}},
            {'task': 'task_d', 'config': {'in_int': 3}},
            {'task': 'task_d', 'name': 'my_task'},
            {'task': 'task_b', 'inputs': {'in_int': '$output.task_d.out_int'}}
            ]})
        self.check_compile(input_str, expected_job_description)

    def test_env_variable(self):
        input_str = """
        from irisml.compiler import get_env
        from irisml.tasks import task_a

        def main():
            int_value = get_env('INT_VALUE')
            task_a(in_int=int_value)
        """
        expected_job_description = JobDescription.from_dict({'tasks': [{'task': 'task_a', 'config': {'in_int': '$env.INT_VALUE'}}]})
        self.check_compile(input_str, expected_job_description)

    def test_function_call(self):
        inputs_str = """
        from irisml.tasks import task_a, task_b

        def my_func(int_value):
            return task_b(in_int=int_value)

        def main():
            output = task_a()
            my_func(int_value=output.out_int)
        """
        expected_job_description = JobDescription.from_dict({'tasks': [
            {'task': 'task_a'},
            {'task': 'task_b', 'inputs': {'in_int': '$output.task_a.out_int'}}]})
        self.check_compile(inputs_str, expected_job_description)

    def test_on_error(self):
        input_str = """
        from irisml.tasks import task_a
        from irisml.compiler import on_error

        def main():
            task_a()
            on_error(lambda: task_a())
        """
        expected_job_description = JobDescription.from_dict({'tasks': [{'task': 'task_a'}], 'on_error': [{'task': 'task_a'}]})
        self.check_compile(input_str, expected_job_description)

    def test_child_tasks(self):
        input_str = """
        from irisml.compiler import make_tasks
        from irisml.tasks import task_a, task_c

        def main():
            tasks = make_tasks(lambda: task_a())
            task_c(tasks=tasks)
        """
        expected_job_description = JobDescription.from_dict({'tasks': [{'task': 'task_c', 'config': {'tasks': [{'task': 'task_a'}]}}]})
        self.check_compile(input_str, expected_job_description)

    def test_child_tasks_with_args(self):
        input_str = """
        from irisml.compiler import make_tasks
        from irisml.tasks import task_a, task_b, task_c

        def child_tasks(int_value):
            task_b(in_int=int_value)

        def main():
            output = task_a()
            tasks = make_tasks(child_tasks, int_value=output.out_int)
            task_c(tasks=tasks)
        """
        expected_job_description = JobDescription.from_dict({'tasks': [
            {'task': 'task_a'},
            {'task': 'task_c', 'config': {'tasks': [{'task': 'task_b', 'inputs': {'in_int': '$output.task_a.out_int'}}]}}]})
        self.check_compile(input_str, expected_job_description)

    def check_compile(self, input_str, expected_job_description, build_args={}):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir = pathlib.Path(temp_dir)
            self._make_fake_tasks(temp_dir)
            input_filepath = temp_dir / 'input.py'
            input_filepath.write_text(textwrap.dedent(input_str))
            compiler = Compiler()
            job_description = compiler.compile(input_filepath, include_paths=[], build_args=build_args)
            print(job_description)
            self.assertEqual(job_description, expected_job_description)

    def test_build_args(self):
        input_str = """
        from irisml.tasks import task_a, task_b

        def main(param, param2, param3):
            if param == '1' and param2 == "single quotes 'hi'" and param3 == 'double quotes ""':
                output = task_a()
                output = task_b(in_int=output.out_int)
        """
        expected_job_description = JobDescription.from_dict({'tasks': [
            {'task': 'task_a'},
            {'task': 'task_b', 'inputs': {'in_int': '$output.task_a.out_int'}}]})

        self.check_compile(input_str, expected_job_description, {'param': '1', 'param2': "single quotes 'hi'", 'param3': 'double quotes ""'})

    def test_match(self):
        input_str = """
        from irisml.tasks import task_a, task_b
        from irisml.compiler import make_patch

        def main():
            make_patch(match=lambda: task_a(), remove=True)
            make_patch(match=lambda: task_a(_name='my_task'), remove=True)
            make_patch(match=lambda: task_a(in_int=3), remove=True)
            make_patch(match=lambda: task_a(in_int=3, _name='my_task'), remove=True)
            make_patch(match=lambda: task_a() and task_b(), remove=True)
        """
        self._check_patch_compile(input_str, {'patches': [{'match': [{'task': 'task_a'}], 'remove': True},
                                                          {'match': [{'task': 'task_a', 'name': 'my_task'}], 'remove': True},
                                                          {'match': [{'task': 'task_a', 'config': {'in_int': 3}}], 'remove': True},
                                                          {'match': [{'task': 'task_a', 'name': 'my_task', 'config': {'in_int': 3}}], 'remove': True},
                                                          {'match': [{'task': 'task_a'}, {'task': 'task_b'}], 'remove': True}]})

    def test_match_if_exists(self):
        input_str = """
        from irisml.tasks import task_a
        from irisml.compiler import make_patch

        def main():
            make_patch(match_if_exists=lambda: task_a(), remove=True)
        """
        self._check_patch_compile(input_str, {'patches': [{'match_if_exists': [{'task': 'task_a'}], 'remove': True}]})

    def test_match_oneof(self):
        input_str = """
        from irisml.tasks import task_a, task_b
        from irisml.compiler import make_patch

        def main():
            make_patch(match_oneof=[lambda: task_a(), lambda: task_b()], remove=True)
        """
        self._check_patch_compile(input_str, {'patches': [{'match_oneof': [[{'task': 'task_a'}], [{'task': 'task_b'}]], 'remove': True}]})

    def test_insert(self):
        input_str = """
        from irisml.tasks import task_a, task_b
        from irisml.compiler import make_patch, get_env

        def main():
            make_patch(top=True, insert=lambda: task_a())
            make_patch(top=True, insert=lambda: task_a() and task_b())
            make_patch(bottom=True, insert=lambda: task_a(_name='my_task'))
            make_patch(bottom=True, insert=lambda: task_a(in_int=3))
            make_patch(match=lambda: task_a(), insert=lambda: task_b())
            make_patch(top=True, insert=lambda: task_a(in_int=get_env("INT_VALUE")))
        """
        self._check_patch_compile(input_str, {'patches': [{'top': True, 'insert': [{'task': 'task_a'}]},
                                                          {'top': True, 'insert': [{'task': 'task_a'}, {'task': 'task_b'}]},
                                                          {'bottom': True, 'insert': [{'task': 'task_a', 'name': 'my_task'}]},
                                                          {'bottom': True, 'insert': [{'task': 'task_a', 'config': {'in_int': 3}}]},
                                                          {'match': [{'task': 'task_a'}], 'insert': [{'task': 'task_b'}]},
                                                          {'top': True, 'insert': [{'task': 'task_a', 'config': {'in_int': '$env.INT_VALUE'}}]}]})

    def test_replace(self):
        input_str = """
        from irisml.tasks import task_a, task_b
        from irisml.compiler import make_patch

        def main():
            make_patch(match=lambda: task_a(), replace=(lambda: task_b(), {}))
            make_patch(match=lambda: task_a(), replace=(lambda: task_b() and task_a(), {}))
            make_patch(match=lambda: task_a(), replace=(lambda: task_b(), {'task_a.out': 'task_b.out'}))
        """
        self._check_patch_compile(input_str, {'patches': [{'match': [{'task': 'task_a'}], 'replace': ([{'task': 'task_b'}], {})},
                                                          {'match': [{'task': 'task_a'}], 'replace': ([{'task': 'task_b'}, {'task': 'task_a'}], {})},
                                                          {'match': [{'task': 'task_a'}], 'replace': ([{'task': 'task_b'}], {'task_a.out': 'task_b.out'})}]})

    def test_update(self):
        input_str = """
        from irisml.tasks import task_a, task_b
        from irisml.compiler import make_patch, get_env

        def main():
            make_patch(match=lambda: task_a(), update={'in_int': 3})
            make_patch(match=lambda: task_a(), update={'in_int': get_env("INT_VALUE")})
        """
        self._check_patch_compile(input_str, {'patches': [
            {'match': [{'task': 'task_a'}], 'update': {'in_int': 3}},
            {'match': [{'task': 'task_a'}], 'update': {'in_int': '$env.INT_VALUE'}}
            ]})

    def test_patch_on_error(self):
        input_str = """
        from irisml.tasks import task_a
        from irisml.compiler import make_patch

        def main():
            make_patch(match=lambda: task_a(), remove=True, on_error=True)
        """
        self._check_patch_compile(input_str, {'patches_on_error': [{'match': [{'task': 'task_a'}], 'remove': True}]})

    def test_top_bottom(self):
        input_str = """
        from irisml.tasks import task_a, task_b
        from irisml.compiler import make_patch

        def main():
            make_patch(top=True, insert=lambda: task_a())
            make_patch(bottom=True, insert=lambda: task_b())
        """
        self._check_patch_compile(input_str, {'patches': [{'top': True, 'insert': [{'task': 'task_a'}]},
                                                          {'bottom': True, 'insert': [{'task': 'task_b'}]}]})

    def _make_fake_tasks(self, dir_path):
        tasks_dir = dir_path / 'irisml' / 'tasks'
        tasks_dir.mkdir(parents=True)

        (tasks_dir / 'task_a.py').write_text(textwrap.dedent("""
        import dataclasses
        import irisml.core

        class Task(irisml.core.TaskBase):
            CACHE_ENABLED = False
            @dataclasses.dataclass
            class Config:
                in_int: int = 100

            @dataclasses.dataclass
            class Outputs:
                out_int: int = 42
        """))

        (tasks_dir / 'task_b.py').write_text(textwrap.dedent("""
        import dataclasses
        import irisml.core

        class Task(irisml.core.TaskBase):
            CACHE_ENABLED = False
            @dataclasses.dataclass
            class Inputs:
                in_int: int
        """))

        (tasks_dir / 'task_c.py').write_text(textwrap.dedent("""
        import dataclasses
        import typing
        from irisml.core import TaskDescription
        import irisml.core

        class Task(irisml.core.TaskBase):
            CACHE_ENABLED = False
            @dataclasses.dataclass
            class Config:
                tasks: typing.List[TaskDescription]
        """))

        (tasks_dir / 'task_d.py').write_text(textwrap.dedent("""
        import dataclasses
        import typing
        from irisml.core import TaskDescription
        import irisml.core

        class Task(irisml.core.TaskBase):
            @dataclasses.dataclass
            class Config:
                in_int: int = 100

            @dataclasses.dataclass
            class Outputs:
                out_int: int = 42
        """))

    def _compile(self, input_str):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir = pathlib.Path(temp_dir)
            self._make_fake_tasks(temp_dir)
            input_filepath = temp_dir / 'input.py'
            input_filepath.write_text(textwrap.dedent(input_str))
            compiler = Compiler()
            patch_description = compiler.compile(input_filepath, include_paths=[], build_args={})
            print(patch_description)
            return patch_description

    def _check_patch_compile(self, input_str, expected_patch_dict):
        expected_patch_description = PatchDescription.from_dict(expected_patch_dict)
        generated = self._compile(input_str)
        self.assertEqual(generated, expected_patch_description)
