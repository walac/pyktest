from . import util
import os
import platform
from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class Make:
    """A wrapper to the make command.

    Constructor arguments:

        :param srcdir: The kernel source directory path.
        :type srcdir: str
        :param outdir: The binary output directory.
        :type outdir: str
        :param arch: The target binary architecture.
        :type arch: str
        :param make: The make command.
        :type make: str
    """

    srcdir: str
    outdir: str
    arch: str = field(default_factory=platform.machine)
    make: str = "make"

    def __call__(self, target='', args='', parallel: bool = False) -> None:
        """Call the make command.

        :param target: the make command target
        :type target: str
        :param args: additional arguments to the make command
        :type args: str
        :param parallel: if True, will run os.cpu_count() instances of the make `-j$(nproc)`
        :type parallel: bool

        :raise subprocess.CalledProcessorError: if the command fails

        :rtype: None
        """
        j = f'-j{os.cpu_count()}' if parallel else ''
        util.run_cmd(
            f'{self.make} ARCH={self.arch} O={self.outdir} {j} {args} {target}',
            cwd=self.srcdir)

    def kernel_release(self) -> str:
        """Compute the kernel release.

        :raise subprocess.CalledProcessorError: if the command fails

        :return: A string with the kernel release
        :rtype: str
        """
        return util.run_cmd(f'{self.make} kernelrelease',
                            capture_output=True,
                            cwd=self.srcdir).rstrip('\n')


__all__ = ['Make']