from typing import Callable
from abc import ABC, abstractmethod


class Connection(ABC):
    """
    Interface to a remote host.

    A Connection interface is an API to interact with
    the remote host.
    """

    @abstractmethod
    def run_command(self, cmd: str, capture_output=False) -> str:
        """
        Run a command in the remote host.

        :param cmd: The command to run.
        :type cmd: str
        :param capture_output: Should we return the command output?
        :type capture_output: bool
        :return: if capture_output is True, return the command output,
                 otherwise return an empty string.
        :rtype: str
        :raise subprocess.CalledprocessorError: if the command fails.
        """

    @abstractmethod
    def copy_to(self, src: str, dest: str) -> None:
        """
        Copy a local file to the host.

        :param src: The local source file.
        :type src: str
        :param dest: The destination path in the host.
        :type dest: str
        :rtype: None
        """

    @abstractmethod
    def copy_from(self, src: str, dest='.') -> None:
        """
        Copy a file from the host to the local machine.

        :param src: The remote source file.
        :type src: str
        :param dest: The destination path in the local machine.
        :type dest: str
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

    def run_command(self, cmd: str, capture_output=False) -> str:
        super().run_command(cmd, capture_output)
        raise NotImplemented('run_command is not implemented')

    def copy_to(self, src: str, dest: str) -> None:
        super().copy_to(src, dest)
        raise NotImplementedError('copy_to is not implemented')

    def copy_from(self, src: str, dest='.') -> None:
        super().copy_from(src, dest)
        raise NotImplementedError('copy_from is not implemented')


class NullFactory(ConnectionFactory):
    """Factory for NullConnection."""

    def create_connection(self) -> Connection:
        return NullConnection()


FactoryType = Callable[[], Connection]

__all__ = [
    'FactoryType', 'Connection', 'ConnectionFactory', 'NullConnection',
    'NullFactory'
]
