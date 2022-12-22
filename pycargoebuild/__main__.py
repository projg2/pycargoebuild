import argparse
import io
import logging
import os.path
import shutil
import sys
import tempfile
import typing

from pathlib import Path

from pycargoebuild.cargo import Crate, get_crates, get_package_metadata
from pycargoebuild.ebuild import get_ebuild, update_ebuild
from pycargoebuild.fetch import (fetch_crates_using_wget,
                                 fetch_crates_using_aria2,
                                 verify_crates)
from pycargoebuild.license import load_license_mapping


FETCHERS = ("aria2", "wget")


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
    argp.add_argument("directory",
                      type=Path,
                      default=[Path(".")],
                      nargs="*",
                      help="Directory containing Cargo.* files (default: .)")
    args = argp.parse_args(argv)

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

    def iterate_parents(directory: Path) -> typing.Generator[Path, None, None]:
        root = directory.absolute().root
        yield directory
        while not directory.samefile(root):
            directory /= ".."
            yield directory

    def get_cargo_lock_file(directory: Path) -> io.BufferedReader:
        err: typing.Optional[Exception] = None
        for directory in iterate_parents(directory):
            try:
                return open(directory / "Cargo.lock", "rb")
            except FileNotFoundError as e:
                if err is None:
                    err = e
        raise RuntimeError(
            "Cargo.lock not found in any of the parent directories") from err

    crates: typing.Set[Crate] = set()
    pkg_metas = []
    for directory in args.directory:
        with open(directory / "Cargo.toml", "rb") as f:
            pkg_metas.append(get_package_metadata(f))
        with get_cargo_lock_file(directory) as f:
            crates.update(get_crates(f))
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

    def try_fetcher(name: str, func: typing.Callable[..., None]) -> bool:
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

    if (not try_fetcher("aria2", fetch_crates_using_aria2) and
            not try_fetcher("wget", fetch_crates_using_wget)):
        if args.fetcher == "auto":
            raise RuntimeError(
                f"No supported fetcher found (out of {', '.join(FETCHERS)})")
        assert False, f"Unexpected args.fetcher={args.fetcher}"
    verify_crates(crates, distdir=args.distdir)
    crate_files = [args.distdir / crate.filename for crate in crates]

    if args.input is not None:
        ebuild = update_ebuild(args.input.read(),
                               pkg_meta,
                               crate_files,
                               crate_license=not args.no_license)
        logging.warning(
            "The in-place mode updates CRATES and crate LICENSE+= variables "
            "only, other metadata is left unchanged")
    else:
        ebuild = get_ebuild(pkg_meta,
                            crate_files,
                            crate_license=not args.no_license)

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
