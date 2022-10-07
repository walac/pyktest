from io import StringIO
from os.path import dirname, join
from subprocess import CalledProcessError
from typing import IO, Any
from tempfile import NamedTemporaryFile, gettempdir

import pytest

from ktest.connection import ssh
from ktest.connection import base

from . import sshd


@pytest.fixture(scope='module', autouse=True)
def ssh_server() -> sshd.SSHD:
    return sshd.SSHD()


@pytest.fixture(scope='module')
def factory() -> ssh.ConnectionFactory:
    pkey = join(dirname(__file__), 'pyktest-ssh/fake_keys/id_rsa')
    return ssh.ConnectionFactory(
        ssh.HostConfig(host='localhost',
                       user='root',
                       port=sshd.SSHD.PORT,
                       connect_kwargs={'key_filename': pkey}))


@pytest.fixture
def connection(factory: ssh.ConnectionFactory) -> base.Connection:
    return factory()


@pytest.fixture(scope='module')
def test_str() -> str:
    """Return a generic string for tests."""
    return 'This is a test string'


@pytest.fixture
def tmp_file(test_str: str) -> IO[Any]:
    """Return a temporary file with a test string."""
    tmp = NamedTemporaryFile()
    tmp.write(test_str.encode())
    tmp.flush()
    return tmp


@pytest.fixture
def test_filename() -> str:
    return '/tmp/file.txt'


def test_run_command(connection: base.Connection, log_stream: StringIO,
                     test_str: str) -> None:
    output = connection.run_command(f'echo {test_str}')
    assert output == ''
    assert test_str in log_stream.getvalue()

    output = connection.run_command(f'echo -n {test_str}', capture_output=True)
    assert test_str == output

    with pytest.raises(CalledProcessError):
        connection.run_command('ls /invalid')

    with pytest.raises(CalledProcessError):
        connection.run_command('no-command')


def test_put(connection: base.Connection, tmp_file: IO[Any], test_str: str,
             test_filename: str) -> None:
    with tmp_file:
        connection.put(src=tmp_file.name, dest=test_filename)
        file_content = connection.run_command(f'cat {test_filename}',
                                              capture_output=True)
        assert test_str == file_content


def test_get(connection: base.Connection, test_str: str,
             test_filename: str) -> None:
    connection.run_command(f'echo -n {test_str} > {test_filename}')

    dest = join(gettempdir(), 'file.txt')

    connection.get(src=test_filename, dest=dest)

    with open(dest, 'r') as f:
        assert test_str == f.read()
