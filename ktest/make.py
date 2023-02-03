import os
import platform
from dataclasses import dataclass, field

from git.types import PathLike

from . import util


@dataclass(frozen=True, slots=True)
class Make:
    """A wrapper to the make command.

    Constructor arguments:

        :param srcdir: The kernel source directory path.
        :type srcdir: str | os.PathLike
        :param outdir: The binary output directory.
        :type outdir: str | os.PathLike
        :param arch: The target binary architecture.
        :type arch: str
        :param make: The make command.
        :type make: str
    """

    srcdir: PathLike
    outdir: PathLike
    arch: str = field(default_factory=platform.machine)
    make: str = "make"

    def __call__(self, target="", args="", parallel: bool = False) -> None:
        """Call the make command.

        :param target: the make command target
        :type target: str
        :param args: additional arguments to the make command
        :type args: str
        :param parallel: if True, will run os.cpu_count() instances of the make
                         `-j$(nproc)`
        :type parallel: bool

        :raise subprocess.CalledProcessorError: if the command fails

        :rtype: None
        """
        j = f"-j{os.cpu_count()}" if parallel else ""
        util.run_cmd(
            f"{self.make} ARCH={self.arch} O={os.fspath(self.outdir)} {j} {args} "
            + f"{target}",
            cwd=os.fspath(self.srcdir),
        )

    def kernel_release(self) -> str:
        """Compute the kernel release.

        :raise subprocess.CalledProcessorError: if the command fails

        :return: A string with the kernel release
        :rtype: str
        """
        return util.run_cmd(
            f"{self.make} -s kernelrelease",
            capture_output=True,
            cwd=os.fspath(self.srcdir),
        ).rstrip("\n")

    def kernel_version(self) -> str:
        """Compute the kernel version.

        :raise subprocess.CalledProcessorError: if the command fails

        :return: A string with the kernel version
        :rtype: str
        """
        return util.run_cmd(
            f"{self.make} -s kernelversion",
            capture_output=True,
            cwd=os.fspath(self.srcdir),
        ).rstrip("\n")


__all__ = ["Make"]
