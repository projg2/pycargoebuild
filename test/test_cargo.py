import io

import pytest

from pycargoebuild.cargo import (cargo_to_spdx, get_crates,
                                 get_package_metadata, PackageMetadata)

from .testdata import CARGO_LOCK_TOML, CRATES


def test_cargo_to_spdx():
    assert cargo_to_spdx("A/B/C") == "A OR B OR C"


def test_get_crates():
    input_toml = CARGO_LOCK_TOML

    assert get_crates(io.BytesIO(input_toml), exclude=["test"]) == CRATES


@pytest.mark.parametrize("exclude", ["", "description", "homepage"])
def test_get_package_metadata(exclude):
    name = "test"
    version = "1.2.3"
    license = "MIT"
    description = None
    homepage = None

    input_toml = f"""
        [package]
        name = "{name}"
        version = "{version}"
        license = "{license}"
    """

    if exclude != "description":
        description = "A test package"
        input_toml += f'description = "{description}"\n'
    if exclude != "homepage":
        homepage = "https://example.com/test"
        input_toml += f'homepage = "{homepage}"\n'

    assert (get_package_metadata(io.BytesIO(input_toml.encode("utf-8"))) ==
            PackageMetadata(name=name,
                            version=version,
                            description=description,
                            license=license,
                            homepage=homepage))
