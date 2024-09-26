"""Apply a patch to irisml job description.

TODO: Currently this command doesn't update the references to the updated tasks in the job description. We might need to construct a graph of tasks and update the references accordingly.

"""
import argparse
import copy
import json
import logging
import pathlib
from irisml.core.commands.common import configure_logger
from irisml.core.description import JobDescription, PatchDescription, TaskDescription

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description="Apply a patch to irisml job description")
    parser.add_argument('base_filepath', type=pathlib.Path)
    parser.add_argument('patch_filepath', nargs='+', type=pathlib.Path)
    parser.add_argument('--output_filepath', '-o', type=pathlib.Path, default=None)
    parser.add_argument('--verbose', '-v', action='store_true')

    args = parser.parse_args()

    configure_logger(1 if args.verbose else 0)

    base = JobDescription.from_dict(json.loads(args.base_filepath.read_text()))
    for patch_filepath in args.patch_filepath:
        patch = PatchDescription.from_dict(json.loads(patch_filepath.read_text()))
        base = apply_patch(base, patch)

    job_description_json = json.dumps(base.to_dict(), indent=4)
    if args.output_filepath:
        args.output_filepath.parent.mkdir(parents=True, exist_ok=True)
        args.output_filepath.write_text(job_description_json)
    else:
        print(job_description_json)


def _match_task(task, match_condition) -> bool:
    if task.task != match_condition.task:
        return False
    if match_condition.name and task.name != match_condition.name:
        return False
    if match_condition.config:
        for k, v in match_condition.config.items():
            if task.config.get(k) != v:
                return False
    return True


def _from_dict_recusive(x):
    if isinstance(x, dict):
        if 'task' in x:
            try:
                return TaskDescription.from_dict(x)
            except Exception:
                pass
        return {k: _from_dict_recusive(v) for k, v in x.items()}
    if isinstance(x, list):
        return [_from_dict_recusive(v) for v in x]
    if isinstance(x, TaskDescription):
        x.config = _from_dict_recusive(x.config)
        return x
    return x


def _match_tasks(tasks, match_conditions) -> tuple[list[tuple[int, TaskDescription]], list[TaskDescription]] | None:
    """Find the matching tasks in the base job description.

    If no match is found, return None.

    Returns:
        (matched_tasks, container, index_in_container):
            - matched_tasks: The tasks that match the conditions.
            - container: The list in which the matched tasks are found.
            - index_in_container: The index of the first matched task in the container.
    """
    to_search = [tasks]
    target_task_lists = [tasks]
    while to_search:
        next_search = to_search.pop()
        for task in next_search:
            # Check if the task config has List[TaskDescription]
            print(task)
            if task.config:
                for k, v in task.config.items():
                    try:
                        if isinstance(v, list) and v and isinstance(v[0], TaskDescription):
                            target_task_lists.append(v)
                            to_search.append(v)
                    except Exception:
                        pass

    for target_tasks in target_task_lists:
        matched_indexes = set()
        matched = False
        for match_condition in match_conditions:
            matched = False
            for i, task in enumerate(target_tasks):
                if not isinstance(task, TaskDescription):
                    task = TaskDescription.from_dict(task)
                if i not in matched_indexes and _match_task(task, match_condition):
                    matched_indexes.add(i)
                    matched = True
                    break
            if not matched:
                break
        if matched:
            matched_indexes = sorted(list(matched_indexes))
            return [(i, target_tasks[i] if isinstance(target_tasks[i], TaskDescription) else TaskDescription.from_dict(target_tasks[i])) for i in matched_indexes], target_tasks, min(matched_indexes)

    return None


def _replace_output_references(tasks: list[TaskDescription], mappings):
    for task in tasks:
        for k, v in task.inputs.items():
            if isinstance(v, str) and v in mappings:
                task.inputs[k] = mappings[v]
            elif isinstance(v, list) and isinstance(v[0], TaskDescription):
                _replace_output_references(v, mappings)
        for k, v in task.config.items():
            if isinstance(v, str) and v in mappings:
                task.config[k] = mappings[v]
            elif isinstance(v, list) and isinstance(v[0], TaskDescription):
                _replace_output_references(v, mappings)


def _apply_patch_to_tasks(tasks, single_patch):
    match_result = None
    if single_patch.top:
        match_result = ([(0, tasks[0])], tasks)
    elif single_patch.bottom:
        match_result = ([(len(tasks), None)], tasks)
    elif single_patch.match:
        match_result = _match_tasks(tasks, single_patch.match)
    elif single_patch.match_if_exists:
        match_result = _match_tasks(tasks, single_patch.match_if_exists)
        if not match_result:
            return tasks
    elif single_patch.match_oneof:
        for m in single_patch.match_oneof:
            match_result = _match_tasks(tasks, m)
            if match_result:
                break

    if not match_result:
        raise RuntimeError("No tasks matched the conditions in the patch")

    if single_patch.remove:
        for i in reversed([i for i, _ in match_result[0]]):
            del match_result[1][i]
    elif single_patch.update:
        if len(match_result[0]) != 1:
            raise RuntimeError("Exactly one task must be matched for update")
        for c in single_patch.update:
            match_result[0][0][1].config[c] = single_patch.update[c]
            logger.debug(f"Updated task {match_result[0][0][1].task} with config {c}={single_patch.update[c]}")
    elif single_patch.insert:
        for i, t in enumerate(single_patch.insert):
            match_result[1].insert(match_result[0][0][0] + i, t)
            logger.debug(f"Inserted task {t.name} at index {match_result[0][0][0] + i}")
    elif single_patch.replace:
        for i, _ in reversed(match_result[0]):
            del match_result[1][i]
        mappings = {'$output.' + k: '$output.' + v for k, v in single_patch.replace[1].items()}
        _replace_output_references(match_result[1], mappings)
        for i, t in enumerate(single_patch.replace[0]):
            match_result[1].insert(match_result[0][0][0] + i, t)
            logger.debug(f"Inserted task {t.name} at index {match_result[0][0][0] + i}")

    return tasks


def apply_patch(base, patch):
    base = copy.deepcopy(base)
    base.tasks = _from_dict_recusive(base.tasks)
    base.on_error = _from_dict_recusive(base.on_error)

    for p in patch.patches:
        base.tasks = _apply_patch_to_tasks(base.tasks, p)
    for p in patch.patches_on_error:
        base.on_error = _apply_patch_to_tasks(base.on_error, p)

    return base
