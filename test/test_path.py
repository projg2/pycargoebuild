import itertools

import pytest

from pycargoebuild.path import PathWrapper


@pytest.fixture
def test_tree(tmp_path):
    start_dir = tmp_path / "a" / "b"
    start_dir.mkdir(parents=True)
    with open(start_dir / "Cargo.toml", "wb"):
        pass
    with open(tmp_path / "Cargo.lock", "wb"):
        pass
    yield PathWrapper(start_dir)


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
