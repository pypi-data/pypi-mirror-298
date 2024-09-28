"""
This module allows reporting on past or current parameter sweeps.
"""

import logging

from pathlib import Path

from ictasks.tasks import Task, TaskCollection

from iccore.serialization import read_yaml

logger = logging.getLogger()


class ParameterSweepReporter:
    """
    This class is used to report on finished or running parameter sweeps.
    """

    def __init__(
        self,
        result_dir: Path,
        attributes: list | None = None,
    ) -> None:
        self.result_dir = result_dir
        if attributes:
            self.attributes = attributes
        else:
            self.attributes = []

    def task_subset_from_config(self, config_dir: Path) -> TaskCollection:
        config = read_yaml(config_dir)
        tasks = TaskCollection(self.result_dir)
        tasks.load_from_job_dir()
        relevant_tasks = TaskCollection(self.result_dir)
        for task in tasks:
            if self.validate_tasks_parameters(task, config):
                relevant_tasks.add_task(task)
        return relevant_tasks

    def validate_tasks_parameters(self, task: Task, config) -> bool:
        """
        Check that this task's parameters are in line with the upper and lower bounds
        and specific values given in the config.
        """
        for key, value in task.inputs.items():
            if key in config:
                current_parameter = config[key]
                if "range" in current_parameter:
                    value_range = current_parameter["range"]
                    if "lower" in value_range:
                        if value < value_range["lower"]:
                            return False
                    if "upper" in value_range:
                        if value > value_range["upper"]:
                            return False
                if "values" in current_parameter:
                    if value not in current_parameter["values"]:
                        return False
        return True

    def add_attribute(self, attribute: str) -> None:
        self.attributes.append(attribute)

    def add_attributes(self, attributes: list[str]) -> None:
        for attribute in attributes:
            self.add_attribute(attribute)

    def report_unfinished_tasks(self) -> str:
        tasks = TaskCollection(job_dir=self.result_dir)
        tasks.load_from_job_dir()
        unfinished_tasks = []
        for task in tasks:
            if task.status.state != "finished":
                unfinished_tasks.append(task)

        out_str = "Reporting on all unfinished tasks:"
        return f"{out_str}\n{self.report_tasks(unfinished_tasks)}"

    def report_tasks(self, tasks: list[Task]) -> str:
        out_str = ""
        for task in tasks:
            task_str = self.report_task(task)
            out_str = f"{out_str}\n{task_str}"
        return out_str

    def report_task(self, task: Task) -> str:
        if self.attributes:
            out_str = ""
            for att in self.attributes:
                if att == "id":
                    att_val = task.task_id
                if att == "pid":
                    att_val = str(task.status.pid)
                if att == "launch_cmd":
                    att_val = task.launch_cmd
                out_str = f"{out_str}{att}: {att_val}\n"
        else:
            out_str = str(task)
        return out_str
