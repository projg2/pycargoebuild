import logging
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
    crate_license: bool = True
    uses_license_file: bool = False


PACKAGES = {
    "blake3-0.3.3.ebuild": Package(
        url="https://files.pythonhosted.org/packages/7e/88/"
            "271fc900d7e8f091601c01412f3eafb62c62a9ce98091a24a822b4c392c1/"
            "blake3-0.3.3.tar.gz",
        checksum="0a78908b6299fd21dd46eb00fa4592b2"
                 "59ee419d586d545a3b86e1f2e4d0ee6d",
        directories=["blake3-0.3.3"],
        expected_filename="blake3-0.3.3.ebuild"),
    "cryptography-38.0.3.ebuild": Package(
        url="https://files.pythonhosted.org/packages/13/dd/"
            "a9608b7aebe5d2dc0c98a4b2090a6b815628efa46cc1c046b89d8cd25f4c/"
            "cryptography-38.0.3.tar.gz",
        checksum="bfbe6ee19615b07a98b1d2287d6a6073"
                 "f734735b49ee45b11324d85efc4d5cbd",
        directories=["cryptography-38.0.3/src/rust"],
        expected_filename="cryptography-rust-0.1.0.ebuild"),
    "qiskit-terra-0.22.3.ebuild": Package(
        url="https://files.pythonhosted.org/packages/98/11/"
            "afb20dd5af0fcf9d5ca57e4cfb2b0b3b1e73fa9dcd39ece82389b77f428a/"
            "qiskit-terra-0.22.3.tar.gz",
        checksum="4dfd246177883c6d1908ff532e384e9a"
                 "e063ceb61236833ad656e2da9953a387",
        directories=["qiskit-terra-0.22.3"],
        expected_filename="qiskit-terra-0.22.3.ebuild"),
    "rustworkx-0.12.1.ebuild": Package(
        url="https://files.pythonhosted.org/packages/17/e6/"
            "924967efd523c0bfed2868b62c334a3339f21fba0ac4b447089731312159/"
            "rustworkx-0.12.1.tar.gz",
        checksum="13a19a2f64dff086b3bffffb294c4630"
                 "100ecbc13634b4995d9d36a481ae130e",
        directories=["rustworkx-0.12.1"],
        expected_filename="rustworkx-0.12.1.ebuild"),
    "rustls-0.20.7.ebuild": Package(
        url="https://crates.io/api/v1/crates/rustls/0.20.7/download",
        checksum="539a2bfe908f471bfa933876bd1eb6a1"
                 "9cf2176d375f82ef7f99530a40e48c2c",
        directories=["rustls-0.20.7"],
        expected_filename="rustls-0.20.7.ebuild",
        uses_license_file=True),
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
        expected_filename="hello-world-0.1.0.ebuild",
        crate_license=False),
    "watchfiles-0.18.1.ebuild": Package(
        url="https://files.pythonhosted.org/packages/5e/6a/"
            "2760278f309655cc7305392b0bb664738104202bf5d50396eb138258c5ca/"
            "watchfiles-0.18.1.tar.gz",
        checksum="4ec0134a5e31797eb3c6c624dbe9354f"
                 "2a8ee9c720e0b46fc5b7bab472b7c6d4",
        directories=["watchfiles-0.18.1"],
        expected_filename="watchfiles_rust_notify-0.18.1.ebuild"),
    "synapse-0.1.0.ebuild": Package(
        url="https://files.pythonhosted.org/packages/2b/a0/"
            "fda30d4ec70be0ce89db13c121a1ea72127f91b0b2d6ef6a2f27a1bb61f3/"
            "matrix_synapse-1.72.0.tar.gz",
        checksum="52fd58ffd0865793eb96f4c959c971eb"
                 "e724881863ab0dafca445baf89d21714",
        directories=["matrix_synapse-1.72.0/rust"],
        expected_filename="synapse-0.1.0.ebuild"),
}


def normalize_ebuild(path: Path) -> str:
    """Strip the dynamic ebuild header for comparison"""
    return "".join(path.read_text(encoding="utf-8").partition("EAPI=")[1:])


@pytest.mark.parametrize("ebuild", PACKAGES)
def test_integration(tmp_path, capfd, caplog, ebuild):
    caplog.set_level(logging.WARNING)

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
            member_toml = tarf.getmember(f"{directory}/Cargo.toml")
            assert member_toml is not None
            tarf.extract(member_toml, tmp_path, set_attrs=False)
            for current in (PurePosixPath(directory) / "Cargo.lock").parents:
                try:
                    member_lock = tarf.getmember(f"{current}/Cargo.lock")
                except KeyError:
                    continue
                break
            assert member_lock is not None
            tarf.extract(member_lock, tmp_path, set_attrs=False)

    args = ["-d", str(dist_dir),
            "-l", str(test_dir / "license-mapping.conf"),
            "-o", str(tmp_path / "{name}-{version}.ebuild")]
    if not pkg_info.crate_license:
        args.append("-L")
    args += [str(tmp_path / directory) for directory in pkg_info.directories]

    assert main("test", *args) == 0
    stdout, _ = capfd.readouterr()
    assert stdout == str(tmp_path / pkg_info.expected_filename) + "\n"
    assert (normalize_ebuild(tmp_path / pkg_info.expected_filename) ==
            normalize_ebuild(test_dir / ebuild))

    records = set(caplog.records)
    if pkg_info.uses_license_file:
        # we should get a warning about license-file use
        license_file_warnings = [
            rec for rec in records if "uses license-file" in rec.message]
        assert len(license_file_warnings) > 0
        records.difference_update(license_file_warnings)
    if len(pkg_info.directories) > 1:
        # we should get a warning about multiple directories
        multiple_dir_warnings = [
            rec for rec in records if "Multiple directories" in rec.message]
        assert len(multiple_dir_warnings) > 0
        records.difference_update(multiple_dir_warnings)
    assert len(records) == 0
