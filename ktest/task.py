from typing import Callable, Optional, Sequence
from abc import ABC, abstractmethod
from dataclasses import dataclass, InitVar, field

from .context import Context, TaskInterface

PreExecType = Callable[[TaskInterface], None]
PostExecType = Callable[[TaskInterface], None]


@dataclass(frozen=True, unsafe_hash=True, eq=False)
class Task(ABC):
    """
    Represent a task to execute.

    A task represents a step in the testing scenario. Context class maintains
    a dependency graph of tasks. When we call Context.run(), the tasks are
    executed preserving the dependency order.

    Constructor arguments:

        :param ctx: The Context object.
        :type ctx: Context
        :param pre_exec: A callable object that executes before the task.
        :type pre_exec: PreExecType
        :param post_exec: A callable object that executes after the task.
        :type post_exec: PostExecType
        :param dependencies: A list of tasks than we depend on.
        :type dependencies: list
    """
    ctx: Context
    pre_exec: Optional[PreExecType] = field(default=None, repr=False)
    post_exec: Optional[PostExecType] = field(default=None, repr=False)
    dependencies: InitVar[Sequence[TaskInterface]] = tuple()

    def __post_init__(self, dependencies: Sequence[TaskInterface]) -> None:
        self.ctx.add_dependencies(self, *dependencies)

    def __call__(self) -> None:
        """Run the task."""
        if self.pre_exec:
            self.pre_exec(self)

        self.execute()

        if self.post_exec:
            self.post_exec(self)

    @abstractmethod
    def execute(self) -> None:
        """
        Execute the task.

        Derived classes override this method to define their own behavior.
        """


__all__ = ['Task']
