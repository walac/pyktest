import dataclasses

from .connection.base import Connection


@dataclasses.dataclass(frozen=True)
class Grubby:
    """
    A wrapper for the grubby command.

    Constructor parameters:

        :param connection: A Connection object to the remote peer.
        :type connection: Connection
        :param kernel_version: The kernel version.
        :type kernel_version: str
    """

    connection: Connection
    kernel_version: str

    def add_kernel(
        self,
        args="",
        make_default=False,
        copy_default=True,
        title="",
    ) -> None:
        """
        Add a new kernel entry.

        :param args: Kernel command line additional arguments.
        :type args: str
        :param make_default: If true, make this kernel the default entry.
        :type make_default: bool
        :param copy_default: Copy information as much as possible
                             from the current kernel.
        :type copy_default: bool
        :param title: The GRUB menu kernel title.
        :type title: str
        """
        cmdline = f"grubby --add-kernel={self.kernel_version}"

        if args:
            cmdline += f" --args='{args}'"
        if make_default:
            cmdline += " --make-default"
        if copy_default:
            cmdline += " --copy-default"
        if title:
            cmdline += f" --title='{title}'"

        self.connection.run_command(cmdline)

    def add_args(self, args="") -> None:
        """
        Add kernel command line arguments.

        :param args: The kernel command line arguments to add.
        :type args: str
        """
        self.connection.run_command(
            f"grubby --update-kernel={self.kernel_version} --args='{args}'"
        )

    def remove_args(self, args="") -> None:
        """
        Remove kernel command line argumenets.

        :param args: The kernel command line arguments to remove.
        :type args: str
        """
        self.connection.run_command(
            f"grubby --update-kernel={self.kernel_version} --remove-args='{args}'"
        )

    def remove_kernel(self) -> None:
        """Remove the kernel entry."""
        self.connection.run_command(f"grubby --remove-kernel={self.kernel_version}")

    @property
    def defaut_kernel(self) -> str:
        """
        Return the default kernel path.

        :rtype: str
        """
        return self.connection.run_command(
            "grubby --default-kernel", capture_output=True
        ).rstrip("\n")

    @property
    def default_title(self) -> str:
        """
        Return the title of the default kernel.

        :rtype: str
        """
        return self.connection.run_command(
            "grubby --default-title", capture_output=True
        ).rstrip("\n")


__all__ = ["Grubby"]
