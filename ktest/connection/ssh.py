from typing import Iterable
from subprocess import CalledProcessError
from dataclasses import dataclass

import fabric
from invoke.watchers import StreamWatcher
from invoke.exceptions import UnexpectedExit

from . import base
from .. import _log


class OutputLogger(StreamWatcher):
    def submit(self, stream) -> Iterable[str]:
        _log.logger.info(stream)
        return tuple()


@dataclass(frozen=True)
class HostConfig:
    """
    Hold the connection parameters.

    The constructor arguments are the same of the fabric.Connection class.
    """

    host: str
    user: str | None = None
    port: int | None = None
    config: fabric.connection.Config | None = None
    gateway: fabric.Connection | str | None = None
    forward_agent: bool | None = None
    connect_timeout: int | None = None
    connect_kwargs: dict | None = None
    inline_ssh_env: bool | None = None


class Connection(base.Connection):
    """Implement a ssh connection object."""

    def __init__(self, config: HostConfig) -> None:
        """
        :param config: Connection configuration.
        :type config: HostConfig
        """
        self.__connection = fabric.Connection(**config.__dict__)

    def run_command(self, cmd: str, capture_output=False) -> str:
        """
        Run a command in the remote host.

        :param cmd: The command to run.
        :type cmd: str
        :param capture_output: if True, return the output of the command.
        :type capture_output: bool

        :return: If capture_output is True, return the command output.
                 Otherwise, return an empty string.
        :rtype: str

        :raise subprocess.CalledProcessError: in case a failure to run the command
        """
        _log.logger.info(f"Running: ${cmd}")
        try:
            r: fabric.Result = self.__connection.run(
                cmd, echo=True, watchers=(OutputLogger(),)
            )
        except UnexpectedExit as ex:
            r: fabric.Result = ex.result
            _log.logger.error(r.stderr)
            raise CalledProcessError(returncode=r.exited, cmd=r.command) from ex

        if capture_output:
            return r.stdout

        return ""

    def put(self, src: str, dest: str) -> None:
        """
        Send a file through a ssh connection.

        :param src: The path of the local source file.
        :type src: str
        :param dest: The path of the destiny file in the remote host.
        :type dest: str
        """
        _log.logger.info(
            f"Copying {src} to {self.__connection.user}@{self.__connection.host}:{dest}"
        )
        self.__connection.put(local=src, remote=dest, preserve_mode=False)

    def get(self, src: str, dest: str) -> None:
        """
        Receive a file through a ssh connection.

        :param scr: The path of the source file in the remote host.
        :type scr: str
        :param dest: The path of the destiny local file.
        :type dest: str
        """
        _log.logger.info(
            f"Copying {self.__connection.user}@{self.__connection.host}:{dest} to {src}"
        )
        self.__connection.get(local=dest, remote=src, preserve_mode=False)


@dataclass(frozen=True, slots=True)
class ConnectionFactory(base.ConnectionFactory):
    """
    Factory for the ssh Connection class.

    :param config: a HostConfig object containing the connection configuration.
    :type config: HostConfig
    """

    config: HostConfig

    def create_connection(self) -> base.Connection:
        return Connection(self.config)
