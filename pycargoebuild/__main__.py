import argparse
import os.path
import sys

from pathlib import Path

from pycargoebuild.cargo import get_crates, get_package_metadata
from pycargoebuild.ebuild import get_ebuild


def main(prog_name: str, *argv: str) -> int:
    argp = argparse.ArgumentParser(prog=os.path.basename(prog_name))
    argp.add_argument("-d", "--distdir",
                      type=Path,
                      help="Directory to store downloaded crates in "
                           "(default: get from Portage)")
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

    ebuild = get_ebuild(pkg_meta, crates, distdir=args.distdir)

    outfile = Path(args.output.format(name=pkg_meta.name,
                                      version=pkg_meta.version))
    with open(outfile, "w", encoding="utf-8") as f:
        f.write(ebuild)

    print(f"{outfile}", file=sys.stderr)
    return 0


def entry_point() -> None:
    sys.exit(main(*sys.argv))


if __name__ == "__main__":
    entry_point()
