import io
import typing

import pytest

from pycargoebuild.cargo import (Crate, cargo_to_spdx, get_crates,
                                 get_package_metadata, PackageMetadata)


CARGO_LOCK_TOML = b'''
    version = 3

    [[package]]
    name = "libc"
    version = "0.2.124"
    source = "registry+https://github.com/rust-lang/crates.io-index"
    checksum = """21a41fed9d98f27ab1c6d161da622a4f\\
                  a35e8a54a8adc24bbf3ddd0ef70b0e50"""

    [[package]]
    name = "fsevent-sys"
    version = "4.1.0"
    source = "registry+https://github.com/rust-lang/crates.io-index"
    checksum = """76ee7a02da4d231650c7cea31349b889\\
                  be2f45ddb3ef3032d2ec8185f6313fd2"""
    dependencies = [
     "libc",
    ]

    [[package]]
    name = "test"
    version = "1.2.3"
    source = "registry+https://example.com"
    checksum = """76ee7a02da4d231650c7cea31349b889\\
                  be2f45ddb3ef3032d2ec8185f6313fd2"""

    [[package]]
    name = "test"
    version = "1.2.3"
    dependencies = [
     "fsevent-sys",
     "test",
    ]
'''

CRATES = [
    Crate("libc", "0.2.124", "21a41fed9d98f27ab1c6d161da622a4f"
                             "a35e8a54a8adc24bbf3ddd0ef70b0e50"),
    Crate("fsevent-sys", "4.1.0", "76ee7a02da4d231650c7cea31349b889"
                                  "be2f45ddb3ef3032d2ec8185f6313fd2"),
    Crate("test", "1.2.3", "76ee7a02da4d231650c7cea31349b889"
                           "be2f45ddb3ef3032d2ec8185f6313fd2"),
]


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
