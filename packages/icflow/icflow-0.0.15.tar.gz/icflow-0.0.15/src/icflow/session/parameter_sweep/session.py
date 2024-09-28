"""
This module allows a parameter sweep to be performed.
"""

import logging
import datetime
import uuid
import shutil
import os
from pathlib import Path

from iccore.cli_utils import serialize_args
from ictasks.session import Session as TasksSession
from ictasks.tasks import Task

from .config import ParameterSweepConfig

logger = logging.getLogger()


class ParameterSweep:
    """
    This class is used to implement parameter sweeps driven by an input
    config file.
    """

    def __init__(
        self,
        runner: TasksSession,
        config: ParameterSweepConfig,
        config_path: Path,
    ) -> None:

        self.runner = runner
        self.config_path = config_path
        self.config = config

        current_time = datetime.datetime.now().strftime("%Y-%m-%d_%T")
        job_dir = self.runner.tasks.job_dir
        self.task_workdir = job_dir / f"sweep_{self.config.title}_{current_time}"

    def get_task_workdir(self):
        return self.task_workdir

    def get_launch_cmd(self, args: dict):
        flat_args = serialize_args(args)
        return f"{self.config.program} {flat_args}"

    def setup_tasks(self):
        logger.info("Setting up tasks in %s", self.get_task_workdir())
        tasks = []
        for inputs in self.config.get_expanded_parameters():
            task = Task()
            task.launch_cmd = self.get_launch_cmd(inputs)
            task.task_id = str(uuid.uuid4())
            task.job_dir = self.get_task_workdir()
            task.set_inputs(inputs)
            tasks.append(task)
        logger.info("Finished setting up %d tasks", len(tasks))
        return tasks

    def run(self):
        """
        Run a parameter sweep defined by the config.
        """

        os.makedirs(self.task_workdir)
        config_name = self.config_path.name
        shutil.copyfile(self.config_path, self.task_workdir / config_name)

        self.runner.tasks.items = self.setup_tasks()

        self.runner.run()
