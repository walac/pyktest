import subprocess
from typing import Optional, IO
from os.path import expandvars, expanduser

from ._log import logger


def log_output(output: Optional[IO[str]]) -> None:
    """Log the content of an IO object.

    :param output: The IO object.
    :type output: IO

    :rtype: None
    """
    if output:
        for line in output:
            logger.info(line.rstrip('\n'))


def run_cmd(cmd: str, capture_output=False, **kwargs) -> str:
    """
    Run a shell command.

    :param cmd: The command line to execute.
    :type cmd: str
    :param capture_output: Should we return the command output?
    :type capture_output: bool
    :param kwargs: Keyword paramaters compatible with subprocess.Popen

    :raise subprocess.CalledProcessError: If we fail to execute the command.

    :return: If capture_output is True, return the output of the command. Otherwise,
             return an empty string.
    """
    logger.info(cmd)

    with subprocess.Popen(
            cmd,
            shell=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE if capture_output else subprocess.STDOUT,
            **kwargs) as p:

        if capture_output:
            log_output(p.stderr)
        else:
            log_output(p.stdout)

        rc = p.wait()
        if rc:
            raise subprocess.CalledProcessError(rc, p.args)

        if capture_output and p.stdout:
            return ''.join(p.stdout.readlines())

        return ''


def expd(s: str) -> str:
    """
    Expand references to environment variables and home directory.

    This function expands environment variables and home directory
    references inside the string.

    :param s: The string to expand.
    :type s: string

    :return: The string expanded.
    :rtype: str

    >>> import os
    >>> os.environ['MYVAR'] = 'pyktest'
    >>> home = os.environ.get('HOME', '')
    >>> os.environ['HOME'] = '/home/pyktest'
    >>> expd('test string')
    'test string'
    >>> expd('~/$MYVAR')
    '/home/pyktest/pyktest'
    >>> os.environ['HOME'] = home
    """
    return expandvars(expanduser(s))


__all__ = ['log_output', 'run_cmd', 'expd']
