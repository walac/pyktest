from .connection.base import Connection


def grub2reboot(connection: Connection, title: str) -> None:
    """
    Run the grub2reboot command.

    :param connection: A Connection object to the remote peer.
    :type connection: Connection
    :param title: The GRUB menu kernel title.
    :type title: str
    """
    connection.run_command(f"grub2reboot '{title}'")


def title(connection: Connection, kernel_version: str) -> str:
    """
    Get the kernel GRUB menu title from the kernel version.

    :param connection: A Connection object to the remote peer.
    :type connection: Connection
    :param kernel_version: The kernel version.
    :type kernel_version: str

    :return: The GRUB title entry.
    :rtype: str
    """
    machine_id = connection.run_command(
        "cat /etc/machine-id", capture_output=True
    ).removesuffix("\n")

    return " ".join(
        connection.run_command(
            f"grep -F title /boot/loader/entries/{machine_id}-{kernel_version}.conf"
        )
        .rstrip("\n")
        .split()[1:]
    )


__all__ = ["grub2reboot", "title"]
