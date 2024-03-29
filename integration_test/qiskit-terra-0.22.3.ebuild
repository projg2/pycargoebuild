# Copyright 2023 Gentoo Authors
# Distributed under the terms of the GNU General Public License v2

# Autogenerated by pycargoebuild 0.6.3

EAPI=8

CRATES="
	ahash@0.7.6
	ahash@0.8.0
	autocfg@1.1.0
	bitflags@1.3.2
	cfg-if@1.0.0
	crossbeam-channel@0.5.6
	crossbeam-deque@0.8.2
	crossbeam-epoch@0.9.13
	crossbeam-utils@0.8.14
	either@1.8.0
	fixedbitset@0.4.2
	getrandom@0.2.8
	hashbrown@0.11.2
	hashbrown@0.12.3
	hermit-abi@0.1.19
	indexmap@1.9.2
	indoc@1.0.7
	libc@0.2.137
	libm@0.2.6
	lock_api@0.4.9
	matrixmultiply@0.3.2
	memoffset@0.6.5
	memoffset@0.7.1
	ndarray@0.15.6
	num-bigint@0.4.3
	num-complex@0.4.2
	num-integer@0.1.45
	num-traits@0.2.15
	num_cpus@1.14.0
	numpy@0.17.2
	once_cell@1.16.0
	parking_lot@0.12.1
	parking_lot_core@0.9.4
	petgraph@0.6.2
	ppv-lite86@0.2.17
	proc-macro2@1.0.47
	pyo3-build-config@0.17.3
	pyo3-ffi@0.17.3
	pyo3-macros-backend@0.17.3
	pyo3-macros@0.17.3
	pyo3@0.17.3
	quote@1.0.21
	rand@0.8.5
	rand_chacha@0.3.1
	rand_core@0.6.4
	rand_distr@0.4.3
	rand_pcg@0.3.1
	rawpointer@0.2.1
	rayon-core@1.10.1
	rayon@1.6.0
	redox_syscall@0.2.16
	retworkx-core@0.11.0
	scopeguard@1.1.0
	smallvec@1.10.0
	syn@1.0.103
	target-lexicon@0.12.5
	unicode-ident@1.0.5
	unindent@0.1.10
	version_check@0.9.4
	wasi@0.11.0+wasi-snapshot-preview1
	windows-sys@0.42.0
	windows_aarch64_gnullvm@0.42.0
	windows_aarch64_msvc@0.42.0
	windows_i686_gnu@0.42.0
	windows_i686_msvc@0.42.0
	windows_x86_64_gnu@0.42.0
	windows_x86_64_gnullvm@0.42.0
	windows_x86_64_msvc@0.42.0
"

inherit cargo

DESCRIPTION=""
HOMEPAGE=""
SRC_URI="
	${CARGO_CRATE_URIS}
"

LICENSE=""
# Dependent crate licenses
LICENSE+="
	Apache-2.0 Apache-2.0-with-LLVM-exceptions BSD-2 MIT
	Unicode-DFS-2016
"
SLOT="0"
KEYWORDS="~amd64"
