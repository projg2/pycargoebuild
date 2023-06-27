import dataclasses
import functools
import sys
import tarfile
import typing
import urllib.parse

from pathlib import Path, PurePath

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib


CRATE_REGISTRY = "registry+https://github.com/rust-lang/crates.io-index"


@dataclasses.dataclass(frozen=True)
class Crate:
    name: str
    version: str

    @property
    def filename(self) -> str:
        return f"{self.name}-{self.version}.crate"

    def get_package_directory(self, distdir: Path) -> PurePath:
        return PurePath(f"{self.name}-{self.version}")

    @property
    def download_url(self) -> str:
        raise NotImplementedError()


@dataclasses.dataclass(frozen=True)
class FileCrate(Crate):
    checksum: str

    @property
    def download_url(self) -> str:
        return (f"https://crates.io/api/v1/crates/{self.name}/{self.version}/"
                "download")

    @property
    def crate_entry(self) -> str:
        return f"{self.name}@{self.version}"


@dataclasses.dataclass(frozen=True)
class GitCrate(Crate):
    repository: str
    commit: str

    @property
    def download_url(self) -> str:
        return f"{self.repository}/archive/{self.commit}.tar.gz"

    @property
    def filename(self) -> str:
        return f"{self.repository.rpartition('/')[2]}-{self.commit}.gh.tar.gz"

    @functools.cache
    def get_package_directory(self, distdir: Path) -> PurePath:
        # TODO: perhaps it'd be more correct to follow workspaces
        with tarfile.open(distdir / self.filename, "r:gz") as crate_tar:
            while (tar_info := crate_tar.next()) is not None:
                path = PurePath(tar_info.name)
                if path.name == "Cargo.toml":
                    f = crate_tar.extractfile(tar_info)
                    if f is None:
                        continue

                    # tarfile.ExFileObject() is IO[bytes] while tomli/tomllib
                    # expects BinaryIO -- but it actually is compatible
                    # https://github.com/hukkin/tomli/issues/214
                    metadata = get_package_metadata(f)  # type: ignore
                    if (metadata.name == self.name and
                            metadata.version == self.version):
                        return path.parent

        raise RuntimeError(f"Package {self.name} not found in crate "
                           f"{distdir / self.filename}")

    def get_git_crate_entry(self, distdir: Path) -> str:
        subdir = (str(self.get_package_directory(distdir))
                  .replace(self.commit, "%commit%"))
        return f"{self.repository};{self.commit};{subdir}"


class PackageMetadata(typing.NamedTuple):
    name: str
    version: str
    license: typing.Optional[str] = None
    license_file: typing.Optional[str] = None
    description: typing.Optional[str] = None
    homepage: typing.Optional[str] = None

    def with_replaced_license(self, new_license: typing.Optional[str]
                              ) -> "PackageMetadata":
        return PackageMetadata(name=self.name,
                               version=self.version,
                               license=new_license,
                               license_file=None,
                               description=self.description,
                               homepage=self.homepage)


def cargo_to_spdx(license_str: str) -> str:
    """
    Convert deprecated Cargo license string to SPDX-2.0, if necessary.
    """
    return license_str.replace("/", " OR ")


def get_crates(f: typing.BinaryIO) -> typing.Generator[Crate, None, None]:
    """Read crate list from the open ``Cargo.lock`` file"""
    cargo_lock = tomllib.load(f)
    if cargo_lock["version"] != 3:
        raise NotImplementedError(
            f"Cargo.lock version '{cargo_lock['version']} unsupported")

    for p in cargo_lock["package"]:
        # Skip all crates without "source", they should be local.
        if "source" not in p:
            continue

        try:
            if p["source"] == CRATE_REGISTRY:
                yield FileCrate(name=p["name"],
                                version=p["version"],
                                checksum=p["checksum"])
            elif p["source"].startswith("git+https://github.com/"):
                parsed_url = urllib.parse.urlsplit(p["source"])
                if not parsed_url.fragment:
                    raise RuntimeError(
                        "Git crate with no fragment identifier (i.e. commit "
                        f"identifier): {p['source']!r}")
                repo = parsed_url.path.lstrip("/")
                if repo.endswith(".git"):
                    repo = repo[:-4]
                if repo.count("/") != 1:
                    raise RuntimeError(f"Invalid GitHub URL: {p['source']}")
                yield GitCrate(
                    name=p["name"],
                    version=p["version"],
                    repository=f"https://github.com/{repo}",
                    commit=parsed_url.fragment)
            else:
                raise RuntimeError(f"Unsupported crate source: {p['source']}")
        except KeyError as e:
            raise RuntimeError("Incorrect/insufficient metadata for crate: "
                               f"{p!r}") from e


def get_package_metadata(f: typing.BinaryIO) -> PackageMetadata:
    """Read package from the open ``Cargo.toml`` file"""
    cargo_toml = tomllib.load(f)

    if "package" not in cargo_toml and "workspace" in cargo_toml:
        raise RuntimeError(
            "Specified directory seems to be a workspace root, please run "
            "pycargoebuild on one of its members instead: "
            f"{' '.join(cargo_toml['workspace']['members'])}")

    pkg_meta = cargo_toml["package"]
    pkg_license = pkg_meta.get("license")
    if pkg_license is not None:
        pkg_license = cargo_to_spdx(pkg_license)
    return PackageMetadata(
        name=pkg_meta["name"],
        version=pkg_meta["version"],
        license=pkg_license,
        license_file=pkg_meta.get("license-file"),
        description=pkg_meta.get("description"),
        homepage=pkg_meta.get("homepage"))
