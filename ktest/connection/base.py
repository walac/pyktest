from typing import Callable
from abc import ABC, abstractmethod

from git.types import PathLike


class Connection(ABC):
    """
    Interface to a remote host.

    A Connection interface is an API to interact with
    the remote host.
    """

    @abstractmethod
    def run_command(self, cmd: PathLike, capture_output=False) -> str:
        """
        Run a command in the remote host.

        :param cmd: The command to run.
        :type cmd: PathLike
        :param capture_output: Should we return the command output?
        :type capture_output: bool
        :return: if capture_output is True, return the command output,
                 otherwise return an empty string.
        :rtype: str
        :raise subprocess.CalledprocessorError: if the command fails.
        """

    @abstractmethod
    def put(self, src: PathLike, dest: PathLike) -> None:
        """
        Copy a local file to the host.

        :param src: The local source file.
        :type src: PathLike
        :param dest: The destination path in the host.
        :type dest: PathLike
        :rtype: None
        """

    @abstractmethod
    def get(self, src: PathLike, dest: PathLike) -> None:
        """
        Copy a file from the host to the local machine.

        :param src: The remote source file.
        :type src: PathLike
        :param dest: The destination path in the local machine.
        :type dest: PathLike
        :rtype: None
        """


class ConnectionFactory(ABC):
    """Create new Connection object."""

    def __call__(self) -> Connection:
        """
        Make the factory callable.

        :rtype: Connection
        """
        return self.create_connection()

    @abstractmethod
    def create_connection(self) -> Connection:
        """
        Create a new Connection object.

        :return: A new Connection object.
        :rtype: Connection
        """


class NullConnection(Connection):
    """
    A null connection object.

    It will raise NotImplementedError for any method called.
    """

    def run_command(self, cmd: PathLike, capture_output=False) -> str:
        super().run_command(cmd, capture_output)
        raise NotImplementedError("run_command is not implemented")

    def put(self, src: PathLike, dest: PathLike) -> None:
        super().put(src, dest)
        raise NotImplementedError("copy_to is not implemented")

    def get(self, src: PathLike, dest: PathLike) -> None:
        super().get(src, dest)
        raise NotImplementedError("copy_from is not implemented")


class NullFactory(ConnectionFactory):
    """Factory for NullConnection."""

    def create_connection(self) -> Connection:
        return NullConnection()


FactoryType = Callable[[], Connection]

__all__ = [
    "FactoryType",
    "Connection",
    "ConnectionFactory",
    "NullConnection",
    "NullFactory",
]
