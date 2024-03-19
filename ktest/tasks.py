import shutil
from dataclasses import dataclass
from pathlib import Path

from git.refs import Head
from git.types import PathLike

from .util import expd
from .task import Task


@dataclass(frozen=True, unsafe_hash=True)
class Build(Task):
    """
    A task that builds the kernel.

    Constructor arguments:

        :param config: The path to the .config kernel configuration file.
                       If None, it generates the configuration with the
                       defconfig target.
        :type config:  PathLike | None
        :param head: Head to the git commit/branch.
        :type head: Head | None
        :param build_options: Extra options to pass to make.
        :type build_options: str
        :param parallel_build: Build with -j$(nproc).
        :type parallel_build: bool
        :param clean_build: Run mrproper before the build.
        :type clean_build: bool
    """

    config: PathLike | None = None
    head: Head | None = None
    build_options: str = ""
    parallel_build: bool = True
    clean_build: bool = False

    def execute(self) -> None:
        if self.head:
            self.head.checkout()

        if self.clean_build:
            self.ctx.make("mrproper")

        if self.config:
            config = Path(expd(self.config))

            assert config.exists()
            assert config.is_file()

            shutil.copyfile(config, self.ctx.build_dir / ".config")
            self.ctx.make("olddefconfig")
        else:
            self.ctx.make("defconfig")

        self.ctx.make(args=self.build_options, parallel=self.parallel_build)


class Install(Task):
    """
    Install the kernel in the target machine.
    """

    def __init__(self, build: Build, *args, **kwargs) -> None:
        super().__init__(build.ctx, *args, **kwargs)
        self.ctx.add_dependencies(self, build)
        self.build = build
        self.__extension = ".tar.bz2"

    def execute(self):
        target = self.__extension.replace(".", "")
        pkg = self.__pkg_filename()
        dest = Path("/tmp") / pkg

        self.ctx.make(f"{target}-pkg")
        self.ctx.connection.put(src=pkg, dest=dest)
        self.ctx.connection.run_command(f"tar -xjf {dest} -C /")

    def __pkg_filename(self) -> Path:
        release = self.ctx.make.kernel_release()
        arch = self.ctx.make.arch

        if arch == "x86_64":
            arch = "x86"

        return Path(f"{self.ctx.build_dir}/linux-{release}-{arch}.tar.bz2")
