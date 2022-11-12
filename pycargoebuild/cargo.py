import sys
import typing

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib


class Crate(typing.NamedTuple):
    name: str
    version: str
    checksum: str

    @property
    def filename(self) -> str:
        return f"{self.name}-{self.version}.crate"

    @property
    def crates_io_url(self) -> str:
        return (f"https://crates.io/api/v1/crates/{self.name}/{self.version}/"
                "download")


Crates = typing.List[Crate]


class PackageMetadata(typing.NamedTuple):
    name: str
    version: str
    license: typing.Optional[str] = None
    description: typing.Optional[str] = None
    homepage: typing.Optional[str] = None


def cargo_to_spdx(license_str: str) -> str:
    """
    Convert deprecated Cargo license string to SPDX-2.0, if necessary.
    """
    return license_str.replace("/", " OR ")


def get_crates(f: typing.BinaryIO, exclude: typing.Container[str]) -> Crates:
    """Read crate list from the open ``Cargo.lock`` file"""
    cargo_lock = tomllib.load(f)
    if cargo_lock["version"] != 3:
        raise NotImplementedError(
            f"Cargo.lock version '{cargo_lock['version']} unsupported")
    return [Crate(name=p["name"], version=p["version"], checksum=p["checksum"])
            for p in cargo_lock["package"]
            if p["name"] not in exclude]


def get_package_metadata(f: typing.BinaryIO) -> PackageMetadata:
    """Read package from the open ``Cargo.toml`` file"""
    cargo_toml = tomllib.load(f)
    pkg_meta = cargo_toml["package"]
    if "license_file" in pkg_meta:
        raise NotImplementedError("license_file metadata key not supported")
    license = pkg_meta.get("license")
    if license is not None:
        license = cargo_to_spdx(license)
    return PackageMetadata(name=pkg_meta["name"],
                           version=pkg_meta["version"],
                           license=license,
                           description=pkg_meta.get("description"),
                           homepage=pkg_meta.get("homepage"))
