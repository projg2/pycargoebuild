import argparse
import logging
import os.path
import shutil
import sys
import tempfile
import typing

from pathlib import Path

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

from pycargoebuild.cargo import Crate, get_crates, get_package_metadata
from pycargoebuild.ebuild import get_ebuild, update_ebuild
from pycargoebuild.fetch import (fetch_crates_using_wget,
                                 fetch_crates_using_aria2,
                                 verify_crates)
from pycargoebuild.license import load_license_mapping, MAPPING


FETCHERS = ("aria2", "wget")


class WorkspaceData(typing.NamedTuple):
    crates: typing.FrozenSet[Crate]
    workspace_metadata: dict


def main(prog_name: str, *argv: str) -> int:
    argp = argparse.ArgumentParser(prog=os.path.basename(prog_name))
    argp.add_argument("-d", "--distdir",
                      type=Path,
                      help="Directory to store downloaded crates in "
                           "(default: get from Portage)")
    argp.add_argument("-f", "--force",
                      action="store_true",
                      help="Force overwriting the output file")
    argp.add_argument("-F", "--fetcher",
                      choices=("auto",) + FETCHERS,
                      default="auto",
                      help="Fetcher to use (one of: auto [default], "
                           f"{', '.join(FETCHERS)})")
    argp.add_argument("-i", "--input", "--inplace",
                      type=argparse.FileType("r", encoding="utf-8"),
                      metavar="INPUT",
                      help="Update the CRATES and LICENSE variables "
                           "in the specified ebuild instead of creating "
                           "one from scratch")
    argp.add_argument("-l", "--license-mapping",
                      type=argparse.FileType("r", encoding="utf-8"),
                      help="Path to license-mapping.conf file (default: "
                           "get from Portage)")
    argp.add_argument("-L", "--no-license",
                      action="store_true",
                      help="Do not include LICENSEs (e.g. when crates are "
                           "only used at build time")
    argp.add_argument("-o", "--output",
                      help="Ebuild file to write (default: INPUT if --input "
                           "is specified, {name}-{version}.ebuild otherwise)")
    argp.add_argument("--no-config",
                      action="store_true",
                      help="Inhibit loading configuration files")
    argp.add_argument("directory",
                      type=Path,
                      default=[Path(".")],
                      nargs="*",
                      help="Directory containing Cargo.* files (default: .)")
    args = argp.parse_args(argv)

    config_toml = {}
    if not args.no_config:
        config_dirs = os.environ.get("XDG_CONFIG_DIRS", "/etc/xdg").split(":")
        config_dirs.insert(0, os.environ.get("XDG_CONFIG_HOME", "~/.config"))
        for x in config_dirs:
            config_path = Path(os.path.expanduser(x)) / "pycargoebuild.toml"
            try:
                with open(config_path, "rb") as f:
                    config_toml = tomllib.load(f)
            except (FileNotFoundError, NotADirectoryError):
                pass
            except tomllib.TOMLDecodeError as e:
                raise RuntimeError(
                    f"Error parsing configuration file {config_path}") from e
            else:
                logging.info(f"Using configuration file {config_path}")
                break

    # load defaults from config file
    config_toml_paths = config_toml.get("paths", {})
    if args.distdir is None:
        default_distdir = config_toml_paths.get("distdir")
        if default_distdir is not None:
            args.distdir = Path(default_distdir)
    if args.license_mapping is None:
        default_license_mapping = config_toml_paths.get("license-mapping")
        if default_license_mapping is not None:
            args.license_mapping = open(default_license_mapping, "r",
                                        encoding="utf-8")

    if args.distdir is None or args.license_mapping is None:
        from portage import create_trees
        trees = create_trees()
        tree = trees[max(trees)]
        if args.distdir is None:
            args.distdir = Path(tree["porttree"].settings["DISTDIR"])
        if args.license_mapping is None:
            repo = Path(tree["porttree"].dbapi.repositories["gentoo"].location)
            args.license_mapping = open(repo / "metadata/license-mapping.conf",
                                        "r", encoding="utf-8")

    load_license_mapping(args.license_mapping)
    args.license_mapping.close()
    MAPPING.update(
        (k.lower(), v) for k, v
        in config_toml.get("license-mapping", {}).items())

    def iterate_parents(directory: Path) -> typing.Generator[Path, None, None]:
        root = directory.absolute().root
        yield directory
        while not directory.samefile(root):
            directory /= ".."
            yield directory

    def get_workspace_root(directory: Path) -> WorkspaceData:
        err: typing.Optional[Exception] = None
        for directory in iterate_parents(directory):
            try:
                with open(directory / "Cargo.lock", "rb") as cargo_lock:
                    try:
                        with open(directory / "Cargo.toml",
                                  "rb") as cargo_toml:
                            workspace_toml = (
                                tomllib.load(cargo_toml).get("workspace", {})
                                                        .get("package", {}))
                    except FileNotFoundError:
                        workspace_toml = {}

                    return WorkspaceData(
                        crates=frozenset(get_crates(cargo_lock)),
                        workspace_metadata=workspace_toml)
            except FileNotFoundError as e:
                if err is None:
                    err = e
        raise RuntimeError(
            "Cargo.lock not found in any of the parent directories") from err

    def try_fetcher(name: str,
                    func: typing.Callable[..., None],
                    crates: typing.Iterable[Crate],
                    ) -> bool:
        if args.fetcher == "auto":
            try:
                func(crates, distdir=args.distdir)
            except FileNotFoundError:
                return False
        elif args.fetcher == name:
            func(crates, distdir=args.distdir)
        else:
            return False
        return True

    def fetch_crates(crates: typing.Iterable[Crate]) -> None:
        if (not try_fetcher("aria2", fetch_crates_using_aria2, crates) and
                not try_fetcher("wget", fetch_crates_using_wget, crates)):
            if args.fetcher == "auto":
                raise RuntimeError(
                    "No supported fetcher found (out of "
                    f"{', '.join(FETCHERS)})")
            assert False, f"Unexpected args.fetcher={args.fetcher}"

    crates: typing.Set[Crate] = set()
    pkg_metas = []
    for directory in args.directory:
        with open(directory / "Cargo.toml", "rb") as f:
            workspace = get_workspace_root(directory)
            crates.update(workspace.crates)
            pkg_metas.append(
                get_package_metadata(f, workspace.workspace_metadata))
    pkg_meta = pkg_metas[0]

    if args.no_license:
        pkg_meta = pkg_meta.with_replaced_license(None)
    elif len(args.directory) > 1:
        # Combine licenses of multiple packages
        combined_license = " AND ".join(f"( {pkg.license} )"
                                        for pkg in pkg_metas
                                        if pkg.license is not None)
        pkg_meta = pkg_meta.with_replaced_license(
            combined_license or None)

    if args.input is not None and args.output is None:
        # default to overwriting the input file
        outfile = Path(args.input.name)
    else:
        # This warning is only relevant when constructing a new ebuild,
        # as otherwise we do not update other metadata.
        if len(args.directory) > 1:
            logging.warning(
                "Multiple directories passed, all metadata except for LICENSE "
                f"will be taken from the first package, {pkg_meta.name}")
        if args.output is None:
            args.output = "{name}-{version}.ebuild"
        outfile = Path(args.output.format(name=pkg_meta.name,
                                          version=pkg_meta.version))
        if not args.force and outfile.exists():
            print(f"{outfile} exists already, pass -f to overwrite it",
                  file=sys.stderr)
            return 1

    fetch_crates(crates)
    verify_crates(crates, distdir=args.distdir)

    if args.input is not None:
        ebuild = update_ebuild(
            args.input.read(),
            pkg_meta,
            crates,
            distdir=args.distdir,
            crate_license=not args.no_license,
            license_overrides=config_toml.get("license-overrides", {}),
            )
        logging.warning(
            "The in-place mode updates CRATES, GIT_CRATES and crate "
            "LICENSE+= variables only, other metadata is left unchanged")
    else:
        ebuild = get_ebuild(
            pkg_meta,
            crates,
            distdir=args.distdir,
            crate_license=not args.no_license,
            license_overrides=config_toml.get("license-overrides", {}),
            )

    try:
        with tempfile.NamedTemporaryFile(mode="w",
                                         encoding="utf-8",
                                         dir=outfile.parent,
                                         delete=False) as outf:
            if args.input is not None:
                # typeshed is missing fd support in shutil.copymode()
                # https://github.com/python/typeshed/issues/9288
                shutil.copymode(args.input.fileno(),
                                outf.fileno())  # type: ignore
                args.input.close()
            else:
                umask = os.umask(0)
                os.umask(umask)
                os.fchmod(outf.fileno(), 0o666 & ~umask)
            outf.write(ebuild)
    except Exception:
        Path(outf.name).unlink()
        raise
    Path(outf.name).rename(outfile)

    print(f"{outfile}")
    return 0


def entry_point() -> None:
    try:
        from rich.logging import RichHandler
    except ImportError:
        logging.basicConfig(
            format="[{levelname:>7}] {message}",
            level=logging.INFO,
            style="{")
    else:
        logging.basicConfig(
            format="{message}",
            level=logging.INFO,
            style="{",
            handlers=[RichHandler(show_time=False, show_path=False)])

    sys.exit(main(*sys.argv))


if __name__ == "__main__":
    entry_point()
