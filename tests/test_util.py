import pytest
from subprocess import CalledProcessError
from ktest.util import run_cmd, log_output
from ktest._log import logger
from io import StringIO
from logging import StreamHandler, INFO


def test_log_output(log_stream: StringIO) -> None:
    test_str = 'This is a test log'
    log_output(StringIO(test_str))

    assert test_str in log_stream.getvalue()


def test_run_cmd_ret() -> None:
    test_str = 'this is a test'
    output = run_cmd(f'echo {test_str}', capture_output=True)

    assert test_str == output.rstrip('\n')


def test_run_cmd_log(log_stream: StringIO) -> None:
    test_str = 'this is a test'
    run_cmd(f'echo {test_str}')

    assert test_str in log_stream.getvalue()


def test_run_cmd_fail(log_stream: StringIO) -> None:
    with pytest.raises(CalledProcessError):
        run_cmd('ls /invalid-dir')

    assert 'No such file or directory' in log_stream.getvalue()
