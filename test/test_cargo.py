import io
import typing

import pytest

from pycargoebuild.cargo import (cargo_to_spdx, get_crates,
                                 get_package_metadata, PackageMetadata)

from .testdata import CARGO_LOCK_TOML, CRATES


def test_cargo_to_spdx():
    assert cargo_to_spdx("A/B/C") == "A OR B OR C"


def test_get_crates():
    input_toml = CARGO_LOCK_TOML

    assert list(get_crates(io.BytesIO(input_toml), exclude=["test"])) == CRATES


@pytest.mark.parametrize("exclude", ["", "description", "homepage", "license"])
def test_get_package_metadata(exclude):
    data: typing.Dict[str, typing.Optional[str]] = {
        "name": "test",
        "version": "1.2.3",
        "license": "MIT",
        "description": "A test package",
        "homepage": "https://example.com/test",
    }

    for k in exclude.split():
        data[k] = None

    input_toml = "[package]\n"
    for k, v in data.items():
        if v is not None:
            input_toml += f'{k} = "{v}"\n'

    assert (get_package_metadata(io.BytesIO(input_toml.encode("utf-8"))) ==
            PackageMetadata(**data))  # type: ignore


def test_get_package_metadata_workspace():
    input_toml = """
        [package]
        name = "test"
        version = "0"

        [workspace]
        members = [
            "foo",
            "bar",
        ]
    """

    assert (get_package_metadata(io.BytesIO(input_toml.encode("utf-8"))) ==
            PackageMetadata(name="test",
                            version="0",
                            workspace_members=["foo", "bar"]))


def test_get_package_metadata_license_file():
    input_toml = """
        [package]
        name = "test"
        version = "0"
        license-file = "COPYING"
    """

    assert (get_package_metadata(io.BytesIO(input_toml.encode("utf-8"))) ==
            PackageMetadata(name="test",
                            version="0",
                            license_file="COPYING"))
