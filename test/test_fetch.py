import subprocess
import unittest.mock

from pathlib import Path

import pytest

from pycargoebuild.fetch import fetch_crates

from .testdata import CRATES


@pytest.fixture
def mock_fetch():
    with (unittest.mock.patch.object(Path, "mkdir") as mkdir_mock,
          unittest.mock.patch.object(subprocess, "check_call") as call_mock):
        yield call_mock
    mkdir_mock.assert_called()


def test_fetch_wget(mock_fetch):
    test_path = Path("/test/path")
    fetch_crates(CRATES, test_path)
    mock_fetch.assert_has_calls(
        [unittest.mock.call(["wget", "-O", str(test_path / crate.filename),
                             crate.crates_io_url])
         for crate in CRATES])
