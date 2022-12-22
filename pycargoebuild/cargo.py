import sys
import typing

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib


CRATE_REGISTRY = "registry+https://github.com/rust-lang/crates.io-index"


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
        if p["source"] != CRATE_REGISTRY:
            raise RuntimeError(f"Unsupported crate source: {p['source']}")

        try:
            yield Crate(name=p["name"],
                        version=p["version"],
                        checksum=p["checksum"])
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
