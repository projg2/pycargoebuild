import argparse
import os.path
import sys
import tempfile
import typing

from pathlib import Path

from pycargoebuild.cargo import get_crates, get_package_metadata
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
    argp.add_argument("-o", "--output",
                      help="Ebuild file to write (default: INPUT if --input "
                           "is specified, {name}-{version}.ebuild otherwise)")
    argp.add_argument("directory",
                      type=Path,
                      default=Path("."),
                      nargs="?",
                      help="Directory containing Cargo.* files (default: .)")
    args = argp.parse_args(argv)

    load_license_mapping()
    with open(args.directory / "Cargo.toml", "rb") as f:
        pkg_meta = get_package_metadata(f)
    with open(args.directory / "Cargo.lock", "rb") as f:
        crates = get_crates(f, exclude=[pkg_meta.name])

    if args.input is not None and args.output is None:
        # default to overwriting the input file
        outfile = Path(args.input.name)
    else:
        if args.output is None:
            args.output = "{name}-{version}.ebuild"
        outfile = Path(args.output.format(name=pkg_meta.name,
                                          version=pkg_meta.version))
        if not args.force and outfile.exists():
            print(f"{outfile} exists already, pass -f to overwrite it",
                  file=sys.stderr)
            return 1

    if args.distdir is None:
        from portage import create_trees
        trees = create_trees()
        tree = trees[max(trees)]
        args.distdir = Path(tree["porttree"].settings["DISTDIR"])

    def try_fetcher(name: str, func: typing.Callable[..., None]) -> bool:
        if args.fetcher == "auto":
            try:
                func(crates, distdir=args.distdir)
            except FileNotFoundError:
                return False
        elif args.fetcher == name:
            func(crates, distdir=args.distdir)
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
        ebuild = update_ebuild(args.input.read(), pkg_meta, crate_files)
        args.input.close()
    else:
        ebuild = get_ebuild(pkg_meta, crate_files)

    try:
        with tempfile.NamedTemporaryFile(mode="w",
                                         encoding="utf-8",
                                         dir=outfile.parent,
                                         delete=False) as outf:
            outf.write(ebuild)
    except Exception:
        Path(outf.name).unlink()
        raise
    Path(outf.name).rename(outfile)

    print(f"{outfile}", file=sys.stderr)
    return 0


def entry_point() -> None:
    sys.exit(main(*sys.argv))


if __name__ == "__main__":
    entry_point()
