import hashlib
import subprocess
import typing

from pathlib import Path

from pycargoebuild.cargo import Crates


def fetch_crates_using_aria2(crates: Crates, distdir: Path) -> None:
    """
    Fetch specified crates into distdir using aria2c(1)
    """

    distdir.mkdir(parents=True, exist_ok=True)
    crate_urls = [crate.crates_io_url
                  for crate in crates
                  if not (distdir / crate.filename).exists()]
    if crate_urls:
        subprocess.check_call(
            ["aria2c", "-Z", "-d", str(distdir)] + crate_urls)


def fetch_files_using_wget(files: typing.Iterable[typing.Tuple[str, Path]]
                           ) -> None:
    """
    Fetch specified URLs to the specified filenames using wget(1)
    """

    for url, path in files:
        if not path.exists():
            subprocess.check_call(
                ["wget", "-O", str(path), url])


def fetch_crates_using_wget(crates: Crates, distdir: Path) -> None:
    """
    Fetch specified crates into distdir using wget(1)
    """

    distdir.mkdir(parents=True, exist_ok=True)
    fetch_files_using_wget(
        (crate.crates_io_url, distdir / crate.filename) for crate in crates)


def verify_files(files: typing.Iterable[typing.Tuple[Path, str]]) -> None:
    """
    Verify checksums of specified files
    """

    buffer = bytearray(128 * 1024)
    mv = memoryview(buffer)
    for path, checksum in files:
        with open(path, "rb", buffering=0) as f:
            hasher = hashlib.sha256()
            while True:
                rd = f.readinto(mv)
                if rd == 0:
                    break
                hasher.update(mv[:rd])
            if hasher.hexdigest() != checksum:
                raise RuntimeError(
                    f"checksum mismatch for {path}, got: "
                    f"{hasher.hexdigest()}, exp: {checksum}")


def verify_crates(crates: Crates, distdir: Path) -> None:
    """
    Verify checksums of crates fetched into distdir
    """

    verify_files(
        (distdir / crate.filename, crate.checksum) for crate in crates)
