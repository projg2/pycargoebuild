import io
import itertools
import tarfile

import pytest

from pycargoebuild.cargo import Crate
from pycargoebuild.path import PathWrapper, CrateWrapper


@pytest.fixture
def test_tree(tmp_path):
    start_dir = tmp_path / "a" / "b"
    start_dir.mkdir(parents=True)
    with open(start_dir / "Cargo.toml", "wb"):
        pass
    with open(tmp_path / "Cargo.lock", "wb"):
        pass
    yield PathWrapper(start_dir)


@pytest.fixture
def test_crate(tmp_path):
    with tarfile.open(tmp_path / "test-1.crate", "w:gz") as tarf:
        with io.BytesIO(b"test data\n") as f:
            tar_info = tarfile.TarInfo("test-1/Cargo.toml")
            tar_info.size = len(f.getbuffer())
            tarf.addfile(tar_info, f)
    yield CrateWrapper(Crate("test", "1"), tmp_path)


@pytest.mark.parametrize("func", ["open", "find_in_parents_and_open"])
def test_pathwrapper_open(test_tree, func):
    with getattr(test_tree, func)("Cargo.toml") as f:
        assert f.name == str(test_tree.basedir / "Cargo.toml")


def test_pathwrapper_open_in_parents(test_tree):
    with test_tree.find_in_parents_and_open("Cargo.lock") as f:
        assert f.name == str(test_tree.basedir / "../../Cargo.lock")


def test_pathwrapper_iterate_parents(test_tree):
    # make sure we don't hit an infinite recursion
    # NB: we arbitrarily assume we shouldn't be 1024 directories deep
    parents = itertools.islice(test_tree.iterate_parents(), 1024)
    assert len(list(parents)) < 1024


@pytest.mark.parametrize("func", ["open", "find_in_parents_and_open"])
def test_cratewrapper_open(test_crate, func):
    with getattr(test_crate, func)("Cargo.toml") as f:
        assert f.read() == b"test data\n"
