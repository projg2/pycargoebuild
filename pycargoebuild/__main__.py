import argparse
import os.path
import sys

from pathlib import Path

from pycargoebuild.ebuild import get_ebuild

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib


def main(prog_name, *args):
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
    args = argp.parse_args(args)

    with open(args.directory / "Cargo.toml", "rb") as f:
        cargo_toml = tomllib.load(f)
    with open(args.directory / "Cargo.lock", "rb") as f:
        cargo_lock = tomllib.load(f)

    if args.distdir is None:
        from portage import create_trees
        trees = create_trees()
        tree = trees[max(trees)]
        args.distdir = Path(tree["porttree"].settings["DISTDIR"])

    ebuild = get_ebuild(cargo_toml, cargo_lock, distdir=args.distdir)
    pkgmeta = cargo_toml["package"]

    outfile = Path(args.output.format(name=pkgmeta["name"],
                                      version=pkgmeta["version"]))
    with open(outfile, "w", encoding="utf-8") as f:
        f.write(ebuild)

    print(f"{outfile}", file=sys.stderr)
    return 0


def entry_point():
    sys.exit(main(*sys.argv))


if __name__ == "__main__":
    entry_point()
