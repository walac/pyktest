from types import TracebackType
from contextlib import AbstractContextManager
from typing import Final

from podman.domain.containers import Container
from podman.client import PodmanClient


class SSHD(AbstractContextManager):
    """Run a sshd daemon inside a container."""

    PORT: Final[int] = 2022

    def __init__(self) -> None:
        self.client = PodmanClient()
        co = self.client.containers.run(image='docker.io/walac/pyktest-ssh',
                                        remove=True,
                                        auto_remove=True,
                                        ports={'22/tcp': self.PORT},
                                        detach=True)

        assert isinstance(co, Container)
        self.container = co

    def output(self) -> str:
        s = self.container.logs(stderr=False)
        assert isinstance(s, bytes)
        return s.decode('utf8')

    def close(self) -> None:
        self.container.kill()
        self.client.close()

    def __exit__(self, __exc_type: type[BaseException] | None,
                 __exc_value: BaseException | None,
                 __traceback: TracebackType | None) -> bool | None:
        self.close()
        return super().__exit__(__exc_type, __exc_value, __traceback)

    def __del__(self) -> None:
        self.close()


__all__ = ['SSHD']
