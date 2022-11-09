import hashlib
import subprocess
import typing

from pathlib import Path

from pycargoebuild.cargo import Crates


def fetch_crates(crates: Crates, distdir: Path
                 ) -> typing.Generator[Path, None, None]:
    """
    Fetch specified crates into distdir and yield resulting paths
    """

    distdir.mkdir(parents=True, exist_ok=True)
    buffer = bytearray(128 * 1024)
    mv = memoryview(buffer)
    for crate in crates:
        path = distdir / crate.filename
        if not path.exists():
            subprocess.check_call(
                ["wget", "-O", str(path), crate.crates_io_url])
        with open(path, "rb", buffering=0) as f:
            hasher = hashlib.sha256()
            while True:
                rd = f.readinto(mv)
                if rd == 0:
                    break
                hasher.update(mv[:rd])
            assert hasher.hexdigest() == crate.checksum, (
                f"checksum mismatch for {path}, got: {hasher.hexdigest()}, "
                f"exp: {crate.checksum}")
        yield path
