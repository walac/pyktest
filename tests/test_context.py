from typing import Sequence

import pytest

from ktest.context import Context
from ktest.task import Task


class FakeTask(Task):

    def __init__(
        self,
        ctx: Context,
        number: int,
        order: list[int],
        dependencies: Sequence[Task] = tuple()) -> None:
        self.number = number
        self.order = order
        super().__init__(ctx, dependencies=dependencies)

    def __repr__(self) -> str:
        return f'FakeTask({self.number})'

    def execute(self) -> None:
        self.order.append(self.number)


@pytest.fixture
def ctx() -> Context:
    return Context('')


def test_context_order(ctx: Context) -> None:
    order: list[int] = []
    t1 = FakeTask(ctx, 1, order)
    t2 = FakeTask(ctx, 2, order, (t1, ))
    t4 = FakeTask(ctx, 4, order)
    t3 = FakeTask(ctx, 3, order, (t2, ))
    ctx.add_dependencies(t4, t3)
    ctx.run()

    assert order == [1, 2, 3, 4]
