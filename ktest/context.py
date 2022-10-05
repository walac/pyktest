import platform
import os
from typing import Optional, Protocol
from tempfile import TemporaryDirectory, gettempdir
from dataclasses import dataclass
from graphlib import TopologicalSorter

from git.repo import Repo

from .connection.base import FactoryType, NullFactory, Connection
from .util import expd
from .make import Make
from ._log import logger


class TaskInterface(Protocol):
    """Define an expected interface to a Task."""

    def __call__(self) -> None:
        """Execute the task."""


@dataclass(frozen=True, slots=True)
class _FakeTemp:
    """A fake TemporaryDirectory like class."""

    name: str


class Context:

    def __init__(self,
                 repo: Repo,
                 connection_factory: FactoryType = NullFactory(),
                 arch=platform.machine(),
                 temp_dir=gettempdir(),
                 build_dir: Optional[str] = None) -> None:
        """
        :param repo: Kernel git repository.
        :type repo: Repo
        :param connection_factory: A factory of Connection objects.
        :type connection_factory: FactoryType
        :param arch: The target build architecture (equals to `make ARCH=`)
        :type arch: str
        :param temp_dir: The path to the root temporary directory.
        :type temp_dir: str
        :param build_dir: The path to the output binary directory (equals to `make O=`)
        """
        self.__temp_dir = expd(temp_dir)
        os.makedirs(temp_dir, exist_ok=True)

        self.repo = repo

        self.__connection_factory = connection_factory
        self.__connection: Optional[Connection] = None
        self.__graph: TopologicalSorter[TaskInterface] = TopologicalSorter()

        if build_dir:
            build_dir = expd(build_dir)
            os.makedirs(build_dir, exist_ok=True)
            self.__build_dir = _FakeTemp(build_dir)
        else:
            self.__build_dir = TemporaryDirectory(dir=self.__temp_dir)

        assert isinstance(repo.working_dir, str)
        self.make = Make(srcdir=repo.working_dir,
                         outdir=self.__build_dir.name,
                         arch=arch)

        logger.info(f'Source directory: {repo.working_dir}')
        logger.info(f'Build directory: {self.__build_dir}')
        logger.info(f'Temp directory: {self.__temp_dir}')

    @property
    def connection(self) -> Connection:
        """Return the connection object.

        :return: Connection object.
        :rtype: Connection
        """
        if self.__connection is None:
            self.__connection = self.__connection_factory()
        return self.__connection

    @property
    def build_dir(self) -> str:
        """Return the build directory."""
        return self.__build_dir.name

    def add_dependencies(self, task: TaskInterface,
                         *dependencies: TaskInterface) -> None:
        """
        Add new dependencies to the task.


        :param task: The task we are adding dependencies to.
        :type task: Task
        :param dependencies: A List of tasks that task depends on.
        :type dependencies: list[Task]
        """
        self.__graph.add(task, *dependencies)

    def create_temp_dir(self) -> TemporaryDirectory[str]:
        """Create a new temporary directory."""
        return TemporaryDirectory(dir=self.build_dir)

    def run(self) -> None:
        """Run all tasks in proper order."""
        for t in self.__graph.static_order():
            t()


__all__ = ['Context']
