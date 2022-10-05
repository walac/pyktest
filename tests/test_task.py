from git.repo import Repo
from ktest.task import Task
from ktest.context import Context


class FakeTask(Task):

    def __init__(self) -> None:
        self.steps: list[int] = []

        def f(val):
            return lambda _: self.steps.append(val)

        super().__init__(Context(Repo()), pre_exec=f(1), post_exec=f(3))

    def execute(self) -> None:
        self.steps.append(2)


def test_task() -> None:
    """Test if the task executes its steps in the right order."""
    fake_task = FakeTask()
    fake_task()
    assert fake_task.steps == [1, 2, 3]
