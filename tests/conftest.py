from logging import StreamHandler, INFO
from io import StringIO
import copy

import pytest

from ktest._log import logger


def remove_log_handlers() -> None:
    handlers = copy.copy(logger.handlers)
    for h in handlers:
        logger.removeHandler(h)


@pytest.fixture
def log_stream() -> StringIO:
    """Hook the logger in a StringIO object."""
    remove_log_handlers()

    log_stre = StringIO()
    logger.addHandler(StreamHandler(log_stre))
    logger.setLevel(INFO)

    return log_stre
