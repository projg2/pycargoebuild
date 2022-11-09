import io

import pytest

from pycargoebuild.cargo import (cargo_to_spdx, get_crates, Crate,
                                 get_package_metadata, PackageMetadata)


def test_cargo_to_spdx():
    assert cargo_to_spdx("A/B/C") == "A OR B OR C"


def test_get_crates():
    input_toml = b'''
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
        dependencies = [
         "fsevent-sys",
        ]
    '''

    assert get_crates(io.BytesIO(input_toml), exclude=["test"]) == [
        Crate("libc", "0.2.124", "21a41fed9d98f27ab1c6d161da622a4f"
                                 "a35e8a54a8adc24bbf3ddd0ef70b0e50"),
        Crate("fsevent-sys", "4.1.0", "76ee7a02da4d231650c7cea31349b889"
                                      "be2f45ddb3ef3032d2ec8185f6313fd2"),
    ]


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
