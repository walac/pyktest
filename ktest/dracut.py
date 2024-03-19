from .connection.base import Connection


def make_initrd(connection: Connection, kernel_version: str) -> None:
    """
    Create the initramfs for the given kernel version.

    :param connection: The Connection object to the remote peer.
    :type connection: Connection
    :param kernel_version: The target kernel version.
    :type kernel_version: str
    """
    connection.run_command(f"dracut -f --kver {kernel_version}")


__all__ = ["make_initrd"]
