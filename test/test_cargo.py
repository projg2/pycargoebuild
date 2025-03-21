# pycargoebuild
# (c) 2022-2024 Michał Górny <mgorny@gentoo.org>
# SPDX-License-Identifier: GPL-2.0-or-later

import io
import tarfile
import typing
from pathlib import PurePath

import pytest

from pycargoebuild.cargo import (
    FileCrate,
    GitCrate,
    PackageMetadata,
    cargo_to_spdx,
    get_crates,
    get_package_metadata,
)

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
    source = "registry+https://github.com/rust-lang/crates.io-index"
    checksum = """76ee7a02da4d231650c7cea31349b889\\
                  be2f45ddb3ef3032d2ec8185f6313fd2"""

    [[package]]
    name = "test"
    version = "1.2.3"
    dependencies = [
     "fsevent-sys",
     "test",
    ]

    [[package]]
    name = "regex-syntax"
    version = "0.6.28"
    source = """git+https://github.com/01mf02/regex.git/?rev=90eebbd\\
                #90eebbdb9396ca10510130327073a3d596674d04"""

    [[package]]
    name = "virtiofsd"
    version = "1.12.0"
    source = """git+https://gitlab.com/virtio-fs/virtiofsd?tag=v1.12.0\\
                #af439fbf89f53e18021e8d01dbbb7f66ffd824c1"""

    [[package]]
    name = "pipewire"
    version = "0.8.0"
    source = """git+https://gitlab.freedesktop.org/pipewire/pipewire-rs\\
                ?tag=v0.8.0#449bf53f5d5edc8d0be6c0c80bc19d882f712dd7"""
'''

CRATES = [
    FileCrate("libc", "0.2.124", "21a41fed9d98f27ab1c6d161da622a4f"
                                 "a35e8a54a8adc24bbf3ddd0ef70b0e50"),
    FileCrate("fsevent-sys", "4.1.0", "76ee7a02da4d231650c7cea31349b889"
                                      "be2f45ddb3ef3032d2ec8185f6313fd2"),
    FileCrate("test", "1.2.3", "76ee7a02da4d231650c7cea31349b889"
                               "be2f45ddb3ef3032d2ec8185f6313fd2"),
    GitCrate("regex-syntax", "0.6.28",
             "https://github.com/01mf02/regex",
             "90eebbdb9396ca10510130327073a3d596674d04"),
    GitCrate("virtiofsd", "1.12.0",
             "https://gitlab.com/virtio-fs/virtiofsd",
             "af439fbf89f53e18021e8d01dbbb7f66ffd824c1"),
    GitCrate("pipewire", "0.8.0",
             "https://gitlab.freedesktop.org/pipewire/pipewire-rs",
             "449bf53f5d5edc8d0be6c0c80bc19d882f712dd7"),
]


def test_cargo_to_spdx():
    assert cargo_to_spdx("A/B/C") == "A OR B OR C"


def test_get_crates():
    input_toml = CARGO_LOCK_TOML

    assert list(get_crates(io.BytesIO(input_toml))) == CRATES


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


@pytest.mark.parametrize("exclude", ["", "description", "homepage", "license"])
def test_get_package_metadata_workspace(exclude):
    data: typing.Dict[str, typing.Optional[str]] = {
        "version": "1.2.3",
        "license": "MIT",
        "description": "A test package",
        "homepage": "https://example.com/test",
    }

    for k in exclude.split():
        data[k] = None

    input_toml = '[package]\nname = "test"\n'
    for k, v in data.items():
        if v is not None:
            input_toml += f"{k}.workspace = true\n"

    data["name"] = "test"
    assert (get_package_metadata(io.BytesIO(input_toml.encode("utf-8")),
                                 data) ==
            PackageMetadata(**data))  # type: ignore


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


TOP_CARGO_TOML = b"""\
[package]
name = "toplevel"
version = "0.1"
license = "MIT"

[workspace]
members = ["sub"]
"""

SUB_CARGO_TOML = b"""\
[package]
name = "subpkg"
version = "0.1"
license = "MIT"
"""


@pytest.mark.parametrize(
    "name,expected",
    [("toplevel", ""),
     ("subpkg", "sub"),
     ("nonexistent", RuntimeError),
     ])
def test_git_crate_package_directory(tmp_path, name, expected):
    commit = "5ace474ad2e92da836de60afd9014cbae7bdd481"
    crate = GitCrate(name, "0.1",
                     "https://github.com/projg2/pycargoebuild",
                     commit)
    basename = f"pycargoebuild-{commit}"

    with tarfile.open(tmp_path / f"{basename}.gh.tar.gz", "x:gz") as tarf:
        tar_info = tarfile.TarInfo(f"{basename}/Cargo.toml")
        tar_info.size = len(TOP_CARGO_TOML)
        tarf.addfile(tar_info, io.BytesIO(TOP_CARGO_TOML))
        tar_info = tarfile.TarInfo(f"{basename}/sub/Cargo.toml")
        tar_info.size = len(SUB_CARGO_TOML)
        tarf.addfile(tar_info, io.BytesIO(SUB_CARGO_TOML))

    if expected is RuntimeError:
        with pytest.raises(RuntimeError):
            crate.get_package_directory(tmp_path)
    else:
        assert (crate.get_package_directory(tmp_path) ==
                PurePath(basename) / expected)


@pytest.mark.parametrize("have_lock", [False, True])
def test_git_crate_root_directory(tmp_path, have_lock):
    commit = "5ace474ad2e92da836de60afd9014cbae7bdd481"
    crate = GitCrate("pycargoebuild", "0.1",
                     "https://github.com/projg2/pycargoebuild",
                     commit)
    basename = f"pycargoebuild-{commit}"

    with tarfile.open(tmp_path / f"{basename}.gh.tar.gz", "x:gz") as tarf:
        tar_info = tarfile.TarInfo(f"{basename}/Cargo.toml")
        tar_info.size = len(TOP_CARGO_TOML)
        tarf.addfile(tar_info, io.BytesIO(TOP_CARGO_TOML))
        tar_info = tarfile.TarInfo(f"{basename}/sub/Cargo.toml")
        tar_info.size = len(SUB_CARGO_TOML)
        tarf.addfile(tar_info, io.BytesIO(SUB_CARGO_TOML))
        if have_lock:
            tar_info = tarfile.TarInfo(f"{basename}/Cargo.lock")
            tarf.addfile(tar_info, io.BytesIO(b""))

    assert crate.get_root_directory(tmp_path) == PurePath(basename)
