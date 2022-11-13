import tarfile
import typing

from pathlib import Path, PurePosixPath
from urllib.parse import urlparse

import pytest

from pycargoebuild.__main__ import main
from pycargoebuild.fetch import fetch_files_using_wget, verify_files


class Package(typing.NamedTuple):
    url: str
    checksum: str
    directories: typing.List[str]
    expected_filename: str


PACKAGES = {
    "cryptography-38.0.3.ebuild": Package(
        url="https://files.pythonhosted.org/packages/13/dd/"
            "a9608b7aebe5d2dc0c98a4b2090a6b815628efa46cc1c046b89d8cd25f4c/"
            "cryptography-38.0.3.tar.gz",
        checksum="bfbe6ee19615b07a98b1d2287d6a6073"
                 "f734735b49ee45b11324d85efc4d5cbd",
        directories=["cryptography-38.0.3/src/rust"],
        expected_filename="cryptography-rust-0.1.0.ebuild"),
    # FIXME: we need a way to skip crate licenses since crates are used only
    # for tests here
    "setuptools-rust-1.5.2.ebuild": Package(
        url="https://files.pythonhosted.org/packages/99/db/"
            "e4ecb483ffa194d632ed44bda32cb740e564789fed7e56c2be8e2a0e2aa6/"
            "setuptools-rust-1.5.2.tar.gz",
        checksum="d8daccb14dc0eae1b6b6eb3ecef79675"
                 "bd37b4065369f79c35393dd5c55652c7",
        directories=[f"setuptools-rust-1.5.2/examples/{x}"
                     for x in ["hello-world",
                               "hello-world-script",
                               "html-py-ever",
                               "namespace_package",
                               "rust_with_cffi",
                               ]],
        expected_filename="hello-world-0.1.0.ebuild"),
    "watchfiles-0.18.1.ebuild": Package(
        url="https://files.pythonhosted.org/packages/5e/6a/"
            "2760278f309655cc7305392b0bb664738104202bf5d50396eb138258c5ca/"
            "watchfiles-0.18.1.tar.gz",
        checksum="4ec0134a5e31797eb3c6c624dbe9354f"
                 "2a8ee9c720e0b46fc5b7bab472b7c6d4",
        directories=["watchfiles-0.18.1"],
        expected_filename="watchfiles_rust_notify-0.18.1.ebuild"),
}


def normalize_ebuild(path: Path) -> str:
    """Strip the dynamic ebuild header for comparison"""
    return "".join(path.read_text(encoding="utf-8").partition("EAPI=")[1:])


@pytest.mark.parametrize("ebuild", PACKAGES)
def test_integration(tmp_path, capfd, ebuild):
    pkg_info = PACKAGES[ebuild]

    test_dir = Path(__file__).parent
    dist_dir = test_dir / "dist"
    dist_dir.mkdir(exist_ok=True)
    archive_name = PurePosixPath(urlparse(pkg_info.url).path).name
    dist_file = dist_dir / archive_name

    fetch_files_using_wget([(pkg_info.url, dist_file)])
    verify_files([(dist_file, pkg_info.checksum)])
    with tarfile.open(dist_file, "r") as tarf:
        for directory in pkg_info.directories:
            for filename in ("Cargo.lock", "Cargo.toml"):
                member = tarf.getmember(f"{directory}/{filename}")
                assert member is not None
                tarf.extract(member, tmp_path, set_attrs=False)

    assert main(
        "test", "-d", str(dist_dir),
        "-o", str(tmp_path / "{name}-{version}.ebuild"),
        *(str(tmp_path / directory) for directory in pkg_info.directories)
        ) == 0
    stdout, _ = capfd.readouterr()
    assert stdout == str(tmp_path / pkg_info.expected_filename) + "\n"
    assert (normalize_ebuild(tmp_path / pkg_info.expected_filename) ==
            normalize_ebuild(test_dir / ebuild))
