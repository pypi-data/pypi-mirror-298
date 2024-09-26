import argparse
import dataclasses
import importlib
import inspect
import pkgutil
from irisml.core.commands.common import configure_logger


def _print_dataclass(data_class):
    for field in dataclasses.fields(data_class):
        print(f"    {field.name}: {field.type}")


def _print_task_table():
    import irisml.tasks
    names = [name for module_loader, name, ispkg in pkgutil.iter_modules(irisml.tasks.__path__)]
    descriptions = []
    for name in sorted(names):
        task_module = importlib.import_module('irisml.tasks.' + name)
        task_class = task_module.Task
        task_summary = inspect.getdoc(task_class).splitlines()[0]
        descriptions.append((name, task_summary))

    max_name_length = max(len(name) for name, _ in descriptions)

    print(f"| {'Task':<{max_name_length}} | Description |")
    print(f"| {'-' * max_name_length} | ----------- |")
    for name, summary in descriptions:
        print(f"| {name:<{max_name_length}} | {summary} |")

    print(f"\nTotal: {len(descriptions)} tasks")


def main():
    configure_logger()
    parser = argparse.ArgumentParser(description="Show information about a task")
    parser.add_argument('task_name', nargs='?', help="If not provided, shows all available tasks on this environment.")

    args = parser.parse_args()

    if args.task_name:
        task_module = importlib.import_module('irisml.tasks.' + args.task_name)
        task_class = task_module.Task

        task_doc = inspect.getdoc(task_class)
        if task_doc:
            print(task_doc)
        else:
            print("No description found. Please add documentation to the Task class.")

        print("\nConfiguration:")
        _print_dataclass(task_class.Config)

        print("\nInputs:")
        _print_dataclass(task_class.Inputs)

        print("\nOutputs:")
        _print_dataclass(task_class.Outputs)
    else:
        parser.print_usage()
        print("\nAvailable tasks on this environment:\n")
        _print_task_table()


if __name__ == '__main__':
    main()
