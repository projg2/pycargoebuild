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


.. _cargo-ebuild: https://github.com/gentoo/cargo-ebuild/
