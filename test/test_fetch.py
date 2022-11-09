import hashlib
import subprocess
import unittest.mock

from pathlib import Path

import pytest

from pycargoebuild.fetch import fetch_crates, verify_crates

from .testdata import CRATES


@pytest.fixture
def mock_fetch():
    with unittest.mock.patch.object(subprocess, "check_call") as call_mock:
        with unittest.mock.patch.object(Path, "mkdir") as mkdir_mock:
            yield call_mock
    mkdir_mock.assert_called()


def test_fetch_wget(mock_fetch):
    test_path = Path("/test/path")
    fetch_crates(CRATES, test_path)
    mock_fetch.assert_has_calls(
        [unittest.mock.call(["wget", "-O", str(test_path / crate.filename),
                             crate.crates_io_url])
         for crate in CRATES], any_order=True)


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
