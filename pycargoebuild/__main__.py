import argparse
import os.path
import sys
import typing

from pathlib import Path

from pycargoebuild.cargo import get_crates, get_package_metadata
from pycargoebuild.ebuild import get_ebuild
from pycargoebuild.fetch import (fetch_crates_using_wget,
                                 fetch_crates_using_aria2,
                                 verify_crates)


FETCHERS = ("aria2", "wget")


def main(prog_name: str, *argv: str) -> int:
    argp = argparse.ArgumentParser(prog=os.path.basename(prog_name))
    argp.add_argument("-d", "--distdir",
                      type=Path,
                      help="Directory to store downloaded crates in "
                           "(default: get from Portage)")
    argp.add_argument("-F", "--fetcher",
                      choices=("auto",) + FETCHERS,
                      default="auto",
                      help="Fetcher to use (one of: auto [default], "
                           f"{', '.join(FETCHERS)})")
    argp.add_argument("-o", "--output",
                      default="{name}-{version}.ebuild",
                      help="Ebuild file to write (default: "
                           "{name}-{version}.ebuild)")
    argp.add_argument("directory",
                      type=Path,
                      default=Path("."),
                      nargs="?",
                      help="Directory containing Cargo.* files (default: .)")
    args = argp.parse_args(argv)

    with open(args.directory / "Cargo.toml", "rb") as f:
        pkg_meta = get_package_metadata(f)
    with open(args.directory / "Cargo.lock", "rb") as f:
        crates = get_crates(f, exclude=[pkg_meta.name])

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
    ebuild = get_ebuild(pkg_meta, crate_files)

    outfile = Path(args.output.format(name=pkg_meta.name,
                                      version=pkg_meta.version))
    with open(outfile, "w", encoding="utf-8") as outf:
        outf.write(ebuild)

    print(f"{outfile}", file=sys.stderr)
    return 0


def entry_point() -> None:
    sys.exit(main(*sys.argv))


if __name__ == "__main__":
    entry_point()
