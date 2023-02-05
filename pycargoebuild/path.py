import abc
import tarfile
import typing

from pathlib import Path

from pycargoebuild.cargo import Crate


class PathWrapperBase(abc.ABC):
    """Base class for opening files in Path/tarfile instances"""

    @abc.abstractmethod
    def open(self, subpath: str) -> typing.BinaryIO:
        """Open specified file for reading in binary mode"""

    @abc.abstractmethod
    def find_in_parents_and_open(self, filename: str) -> typing.BinaryIO:
        """Try to open specified file in directory or its parents"""


class PathWrapper(PathWrapperBase):
    """PathWrapperBase implementation for pathlib.Path"""

    def __init__(self, basedir: Path) -> None:
        self.basedir = basedir

    def open(self, subpath: str) -> typing.BinaryIO:
        return open(self.basedir / subpath, "rb")

    def iterate_parents(self) -> typing.Generator[Path, None, None]:
        directory = self.basedir
        root = directory.absolute().root
        yield directory
        while not directory.samefile(root):
            directory /= ".."
            yield directory

    def find_in_parents_and_open(self, filename: str) -> typing.BinaryIO:
        err: typing.Optional[Exception] = None
        for directory in self.iterate_parents():
            try:
                return open(directory / filename, "rb")
            except FileNotFoundError as e:
                if err is None:
                    err = e
        assert err is not None
        raise err


class CrateWrapper(PathWrapperBase):
    """PathWrapperBase implementation for Crate"""

    def __init__(self, crate: Crate, distdir: Path) -> None:
        assert crate.filename.endswith(".crate")
        self.crate_name = crate.filename[:-6]
        self.crate_file = tarfile.open(distdir / crate.filename)

    def open(self, subpath: str) -> typing.BinaryIO:
        ret = self.crate_file.extractfile(f"{self.crate_name}/{subpath}")
        assert ret is not None
        return ret  # type: ignore

    def find_in_parents_and_open(self, filename: str) -> typing.BinaryIO:
        return self.open(filename)
