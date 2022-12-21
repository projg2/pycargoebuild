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


class PackageMetadata(typing.NamedTuple):
    name: str
    version: str
    license: typing.Optional[str] = None
    license_file: typing.Optional[str] = None
    description: typing.Optional[str] = None
    homepage: typing.Optional[str] = None
    workspace_members: typing.List[str] = []

    def with_replaced_license(self, new_license: typing.Optional[str]
                              ) -> "PackageMetadata":
        return PackageMetadata(name=self.name,
                               version=self.version,
                               license=new_license,
                               license_file=None,
                               description=self.description,
                               homepage=self.homepage,
                               workspace_members=list(self.workspace_members))


def cargo_to_spdx(license_str: str) -> str:
    """
    Convert deprecated Cargo license string to SPDX-2.0, if necessary.
    """
    return license_str.replace("/", " OR ")


def get_crates(f: typing.BinaryIO, *, exclude: typing.Container[str]
               ) -> typing.Generator[Crate, None, None]:
    """Read crate list from the open ``Cargo.lock`` file"""
    cargo_lock = tomllib.load(f)
    if cargo_lock["version"] != 3:
        raise NotImplementedError(
            f"Cargo.lock version '{cargo_lock['version']} unsupported")

    def crate_from_cargo_lock(p: dict) -> Crate:
        try:
            return Crate(name=p["name"],
                         version=p["version"],
                         checksum=p["checksum"])
        except KeyError as e:
            raise RuntimeError("Incorrect/insufficient metadata for crate: "
                               f"{p!r}") from e

    # Note that technically rust permits using the same name for external
    # and local packages (sic), and e.g. blake3-py uses it.
    # Therefore, skip packages from exclude list only if they do not
    # have external "source" specified.
    return (crate_from_cargo_lock(p)
            for p in cargo_lock["package"]
            if "source" in p or p["name"] not in exclude)


def get_package_metadata(f: typing.BinaryIO) -> PackageMetadata:
    """Read package from the open ``Cargo.toml`` file"""
    cargo_toml = tomllib.load(f)
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
        homepage=pkg_meta.get("homepage"),
        workspace_members=cargo_toml.get("workspace", {}).get("members", []))
