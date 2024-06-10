# pycargoebuild
# (c) 2022-2024 Michał Górny <mgorny@gentoo.org>
# SPDX-License-Identifier: GPL-2.0-or-later

import pytest

from pycargoebuild.cargo import FileCrate
from pycargoebuild.fetch import ChecksumMismatchError, verify_crates

FOO_CSUM = "37d2046a395cbfcb2712ff5c96a727b1966876080047c56717009dbbc235f566"
BAR_CSUM = "22d39d98821d4b60c3fcbd0fead3c873ddd568971cc530070254b769e18623f3"


@pytest.fixture(scope="session")
def test_crates(tmp_path_factory):
    test_dir = tmp_path_factory.mktemp("crates")
    (test_dir / "foo-1.crate").write_bytes(b"test string\n")
    (test_dir / "bar-2.crate").write_bytes(b"other string\n")
    yield test_dir


def test_verify_pass(test_crates):
    verify_crates([FileCrate("foo", "1", FOO_CSUM),
                   FileCrate("bar", "2", BAR_CSUM),
                   ], distdir=test_crates)


def test_verify_fail(test_crates):
    with pytest.raises(ChecksumMismatchError) as e:
        verify_crates([FileCrate("foo", "1", FOO_CSUM),
                       FileCrate("bar", "2", FOO_CSUM),
                       ], distdir=test_crates)

    assert (e.value.path, e.value.current, e.value.expected
            ) == (test_crates / "bar-2.crate", BAR_CSUM, FOO_CSUM)
