import hashlib
import unittest.mock

from pathlib import Path

from pycargoebuild.fetch import verify_crates

from .testdata import CRATES


def hash_mocking_crate_gen(crates):
    for crate in crates:
        with unittest.mock.patch.object(hashlib, "sha256") as digest_mock:
            digest_mock.return_value.hexdigest.return_value = crate.checksum
            yield crate


def test_verify():
    test_path = Path("/test/path")
    with unittest.mock.patch("pycargoebuild.fetch.open",
                             unittest.mock.mock_open()) as open_mock:
        open_mock.return_value.readinto.return_value = 0
        verify_crates(hash_mocking_crate_gen(CRATES), test_path)
    open_mock.assert_has_calls(
        [unittest.mock.call(test_path / crate.filename, "rb", buffering=0)
         for crate in CRATES], any_order=True)
