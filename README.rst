=============
pycargoebuild
=============
:Author: Michał Górny
:License: MIT
:Homepage: https://github.com/projg2/pycargoebuild/


pycargoebuild is a generator for ebuilds using the Cargo infrastructure
of Rust language.  It is primarily meant to aid in keeping the list
of ``CRATES`` and their ``LICENSE`` up-to-date.  It is a rewrite
of the `cargo-ebuild`_ tool in Python, with no actual dependency
on Rust.

pycargoebuild reads ``Cargo.toml`` and ``Cargo.lock`` files in order
to obtain the package's metadata and dependency list, respectively.
Then it fetches all dependent crates into ``DISTDIR`` and reads their
``Cargo.toml`` files to construct the complete list of licenses.
The resulting data can either be used to construct a new ebuild from
a template or to update the values of ``CRATES`` and ``LICENSE``
in an existing ebuild.


Why not cargo-ebuild?
=====================
pycargoebuild has the following features that cargo-ebuild 0.5.2
is missing:

- small size (cargo-ebuild compiles to 5.5M on my system)

- full support for SPDX-2.0 license expressions with boolean
  simplification (whereas cargo-ebuild just dumps all licenses it finds)

- pretty-printing with line wrapping for license expressions

- support for updating ``CRATES`` and crate ``LICENSE`` in existing
  ebuilds (whereas cargo-ebuild can only generate new ebuilds)

- support for combining the data from multiple subpackages (useful
  e.g. in setuptools-rust)

- support for fast crate fetching if ``aria2c`` is installed

- support for skipping crate licenses (e.g. for when Crates are used
  at build/test time only)


Usage
=====
To create a new ebuild, run::

    pycargoebuild <package-directory>

where *package-directory* is the directory containing ``Cargo.toml``.
This creates an ebuild file named after the package name and version
in the current directory, and outputs its name.

To update an existing ebuild, use instead::

    pycargoebuild -i <current-file>.ebuild <package-directory>

Note that the existing file must contain both ``CRATES`` variable
and ``LICENSE+=`` assignment like the following::

    # Dependent crate licenses
    LICENSE+="..."

It is also possible to explicitly specify the output filename using
the ``-o`` option.


Configuration file
==================
pycargoebuild can additionally be configured using
``pycargoebuild.toml`` in one of the XDG config directories
(usually ``~/.config``).  The following example provides a quick summary
of configuration options available::

    [paths]
    # default --distdir, Portage config is used if not set
    distdir = "/var/cache/portage/distfiles"
    # default --license-mapping, "metadata/license-mapping.conf" from
    # ::gentoo repo (via Portage API) is used if not set
    license-mapping = "/var/db/repos/gentoo/metadata/license-mapping.conf"

    [license-overrides]
    # provide an SPDX license string for packages missing the metadata
    nihav_codec_support = "MIT"
    nihav_core = "MIT"
    nihav_duck = "MIT"

    [license-mapping]
    # additional mappings from SPDX licenses to Gentoo licenses
    "LicenseRef-UFL-1.0" = "UbuntuFontLicense-1.0"


.. _cargo-ebuild: https://github.com/gentoo/cargo-ebuild/
