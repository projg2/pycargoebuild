import pytest

from pycargoebuild.cargo import Crate
from pycargoebuild.fetch import verify_crates


@pytest.fixture(scope="session")
def test_crates(tmp_path_factory):
    test_dir = tmp_path_factory.mktemp("crates")
    with open(test_dir / "foo-1.crate", "wb") as f:
        f.write(b"test string\n")
    with open(test_dir / "bar-2.crate", "wb") as f:
        f.write(b"other string\n")
    yield test_dir


def test_verify_pass(test_crates):
    verify_crates([Crate("foo", "1", "37d2046a395cbfcb2712ff5c96a727b1"
                                     "966876080047c56717009dbbc235f566"),
                   Crate("bar", "2", "22d39d98821d4b60c3fcbd0fead3c873"
                                     "ddd568971cc530070254b769e18623f3"),
                   ], distdir=test_crates)


def test_verify_fail(test_crates):
    with pytest.raises(RuntimeError):
        verify_crates([Crate("foo", "1", "37d2046a395cbfcb2712ff5c96a727b1"
                                         "966876080047c56717009dbbc235f566"),
                       Crate("bar", "2", "37d2046a395cbfcb2712ff5c96a727b1"
                                         "966876080047c56717009dbbc235f566"),
                       ], distdir=test_crates)
