# Copyright 2023 Gentoo Authors
# Distributed under the terms of the GNU General Public License v2

# Autogenerated by pycargoebuild 0.8

EAPI=8

CRATES="
	ab_glyph@0.2.21
	ab_glyph_rasterizer@0.1.8
	addr2line@0.19.0
	adler32@1.2.0
	adler@1.0.2
	ahash@0.7.6
	ahash@0.8.3
	aho-corasick@0.7.20
	aho-corasick@1.0.2
	aliasable@0.1.3
	allocator-api2@0.2.15
	alsa-sys@0.3.1
	alsa@0.7.0
	android-activity@0.4.1
	android-properties@0.2.2
	android-tzdata@0.1.1
	android_system_properties@0.1.5
	anstream@0.3.2
	anstyle-parse@0.2.0
	anstyle-query@1.0.0
	anstyle-wincon@1.0.1
	anstyle@1.0.0
	anyhow@1.0.71
	approx@0.5.1
	arboard@3.2.0
	arc-swap@1.6.0
	arrayref@0.3.7
	arrayvec@0.7.4
	ash@0.37.3+1.3.251
	async-channel@1.8.0
	async-io@1.13.0
	async-lock@2.7.0
	atk-sys@0.16.0
	atomic_refcell@0.1.10
	atty@0.2.14
	autocfg@1.1.0
	backtrace@0.3.67
	base64@0.13.1
	base64@0.21.2
	bindgen@0.64.0
	bit-set@0.5.3
	bit-vec@0.6.3
	bitflags@1.3.2
	bitflags@2.3.2
	bitstream-io@1.6.0
	block-buffer@0.10.4
	block-sys@0.1.0-beta.1
	block2@0.2.0-alpha.6
	block@0.1.6
	bstr@1.5.0
	bumpalo@3.13.0
	bytemuck@1.13.1
	bytemuck_derive@1.4.1
	byteorder@1.4.3
	bytes@1.4.0
	cairo-sys-rs@0.16.3
	calloop@0.10.6
	castaway@0.1.2
	cc@1.0.79
	cesu8@1.1.0
	cexpr@0.6.0
	cfg-expr@0.15.2
	cfg-if@1.0.0
	cfg_aliases@0.1.1
	chrono@0.4.26
	clang-sys@1.6.1
	clap@4.3.4
	clap_builder@4.3.4
	clap_derive@4.3.2
	clap_lex@0.5.0
	clipboard-win@4.5.0
	codespan-reporting@0.11.1
	color_quant@1.1.0
	colorchoice@1.0.0
	colored@2.0.0
	com-rs@0.2.1
	combine@4.6.6
	concurrent-queue@2.2.0
	console@0.15.7
	console_error_panic_hook@0.1.7
	convert_case@0.6.0
	cookie-factory@0.3.2
	core-foundation-sys@0.6.2
	core-foundation-sys@0.8.4
	core-foundation@0.9.3
	core-graphics-types@0.1.1
	core-graphics@0.22.3
	coreaudio-rs@0.11.2
	coreaudio-sys@0.2.12
	cpal@0.15.2
	cpufeatures@0.2.8
	crc-catalog@2.2.0
	crc32fast@1.3.2
	crc@3.0.1
	crossbeam-channel@0.5.8
	crossbeam-deque@0.8.3
	crossbeam-epoch@0.9.15
	crossbeam-utils@0.8.16
	crypto-common@0.1.6
	csv-core@0.1.10
	csv@1.2.2
	ctor@0.1.26
	curl-sys@0.4.63+curl-8.1.2
	curl@0.4.44
	d3d12@0.6.0
	darling@0.20.1
	darling_core@0.20.1
	darling_macro@0.20.1
	dasp_sample@0.11.0
	data-encoding@2.4.0
	derive-try-from-primitive@1.0.0
	diff@0.1.13
	digest@0.10.7
	dirs-sys@0.4.1
	dirs@5.0.1
	dispatch@0.2.0
	displaydoc@0.2.4
	dlib@0.5.2
	doc-comment@0.3.3
	downcast-rs@1.2.0
	ecolor@0.22.0
	egui-wgpu@0.22.0
	egui-winit@0.22.0
	egui@0.22.0
	egui_extras@0.22.0
	either@1.8.1
	emath@0.22.0
	embed-resource@2.1.1
	encode_unicode@0.3.6
	encoding_rs@0.8.32
	enum-map-derive@0.11.0
	enum-map@2.5.0
	enumset@1.1.2
	enumset_derive@0.8.1
	env_logger@0.10.0
	epaint@0.22.0
	errno-dragonfly@0.1.2
	errno@0.3.1
	error-code@2.3.1
	euclid@0.22.9
	event-listener@2.5.3
	fastrand@1.9.0
	fdeflate@0.3.0
	flate2@1.0.26
	float_next_after@0.1.5
	fluent-bundle@0.15.2
	fluent-langneg@0.13.0
	fluent-syntax@0.11.0
	fluent-template-macros@0.8.0
	fluent-templates@0.8.0
	fluent@0.16.0
	flume@0.10.14
	fnv@1.0.7
	foreign-types-shared@0.1.1
	foreign-types@0.3.2
	form_urlencoded@1.2.0
	futures-channel@0.3.28
	futures-core@0.3.28
	futures-executor@0.3.28
	futures-io@0.3.28
	futures-lite@1.13.0
	futures-macro@0.3.28
	futures-sink@0.3.28
	futures-task@0.3.28
	futures-util@0.3.28
	futures@0.3.28
	gdk-pixbuf-sys@0.16.3
	gdk-sys@0.16.0
	generational-arena@0.2.9
	generator@0.7.4
	generic-array@0.14.7
	gethostname@0.2.3
	getrandom@0.2.10
	gif@0.12.0
	gimli@0.27.3
	gio-sys@0.16.3
	glib-sys@0.16.3
	glob@0.3.1
	globset@0.4.10
	glow@0.12.2
	gobject-sys@0.16.3
	gpu-alloc-types@0.2.0
	gpu-alloc@0.5.4
	gpu-allocator@0.22.0
	gpu-descriptor-types@0.1.1
	gpu-descriptor@0.2.3
	gtk-sys@0.16.0
	hashbrown@0.12.3
	hashbrown@0.13.2
	hashbrown@0.14.0
	hassle-rs@0.10.0
	heck@0.4.1
	hermit-abi@0.1.19
	hermit-abi@0.2.6
	hermit-abi@0.3.1
	hexf-parse@0.2.1
	home@0.5.5
	http@0.2.9
	humantime@2.1.0
	iana-time-zone-haiku@0.1.2
	iana-time-zone@0.1.57
	ident_case@1.0.1
	idna@0.4.0
	ignore@0.4.20
	image@0.24.6
	indexmap@1.9.3
	indicatif@0.17.5
	insta@1.29.0
	instant@0.1.12
	intl-memoizer@0.5.1
	intl_pluralrules@7.0.2
	io-lifetimes@1.0.11
	is-terminal@0.4.7
	isahc@1.7.2
	itoa@1.0.6
	jni-sys@0.3.0
	jni@0.19.0
	jni@0.20.0
	jni@0.21.1
	jobserver@0.1.26
	jpeg-decoder@0.3.0
	js-sys@0.3.64
	khronos-egl@4.1.0
	lazy_static@1.4.0
	lazycell@1.3.0
	libc@0.2.146
	libflate@1.4.0
	libflate_lz77@1.2.0
	libloading@0.7.4
	libloading@0.8.0
	libm@0.2.7
	libnghttp2-sys@0.1.7+1.45.0
	libtest-mimic@0.6.0
	libz-sys@1.1.9
	linked-hash-map@0.5.6
	linkme-impl@0.3.10
	linkme@0.3.10
	linux-raw-sys@0.3.8
	lock_api@0.4.10
	log@0.4.19
	loom@0.5.6
	lru@0.10.0
	lyon@1.0.1
	lyon_algorithms@1.0.3
	lyon_geom@1.0.4
	lyon_path@1.0.3
	lyon_tessellation@1.0.10
	lzma-rs@0.3.0
	mach2@0.4.1
	malloc_buf@0.0.6
	matchers@0.1.0
	memchr@2.5.0
	memmap2@0.5.10
	memoffset@0.6.5
	memoffset@0.9.0
	metal@0.24.0
	mime@0.3.17
	minimal-lexical@0.2.1
	miniz_oxide@0.6.2
	miniz_oxide@0.7.1
	mio@0.8.8
	naga@0.12.2
	naga_oil@0.7.0
	ndk-context@0.1.1
	ndk-sys@0.4.1+23.1.7779620
	ndk@0.7.0
	nix@0.24.3
	nix@0.25.1
	nohash-hasher@0.2.0
	nom@7.1.3
	nu-ansi-term@0.46.0
	num-bigint@0.4.3
	num-complex@0.4.3
	num-derive@0.3.3
	num-integer@0.1.45
	num-rational@0.4.1
	num-traits@0.2.15
	num_cpus@1.15.0
	num_enum@0.5.11
	num_enum_derive@0.5.11
	number_prefix@0.4.0
	objc-foundation@0.1.1
	objc-sys@0.2.0-beta.2
	objc2-encode@2.0.0-pre.2
	objc2@0.3.0-beta.3.patch-leaks.3
	objc@0.2.7
	objc_exception@0.1.2
	objc_id@0.1.1
	object@0.30.4
	oboe-sys@0.5.0
	oboe@0.5.0
	once_cell@1.18.0
	openssl-probe@0.1.5
	openssl-sys@0.9.88
	option-ext@0.2.0
	orbclient@0.3.45
	os_info@3.7.0
	ouroboros@0.17.0
	ouroboros_macro@0.17.0
	output_vt100@0.1.3
	overload@0.1.1
	owned_ttf_parser@0.19.0
	pango-sys@0.16.3
	parking@2.1.0
	parking_lot@0.12.1
	parking_lot_core@0.9.8
	path-slash@0.2.1
	peeking_take_while@0.1.2
	percent-encoding@2.3.0
	pin-project-internal@1.1.0
	pin-project-lite@0.2.9
	pin-project@1.1.0
	pin-utils@0.1.0
	pkg-config@0.3.27
	png@0.17.9
	polling@2.8.0
	portable-atomic@1.3.3
	pp-rs@0.2.1
	ppv-lite86@0.2.17
	pretty_assertions@1.3.0
	primal-check@0.3.3
	proc-macro-crate@1.3.1
	proc-macro-error-attr@1.0.4
	proc-macro-error@1.0.4
	proc-macro-hack@0.5.20+deprecated
	proc-macro2@1.0.60
	profiling-procmacros@1.0.8
	profiling@1.0.8
	quick-xml@0.29.0
	quote@1.0.28
	rand@0.8.5
	rand_chacha@0.3.1
	rand_core@0.6.4
	range-alloc@0.1.3
	raw-window-handle@0.5.2
	rayon-core@1.11.0
	rayon@1.7.0
	realfft@3.3.0
	redox_syscall@0.2.16
	redox_syscall@0.3.5
	redox_users@0.4.3
	regex-automata@0.1.10
	regex-syntax@0.6.29
	regex-syntax@0.7.2
	regex@1.8.4
	regress@0.6.0
	renderdoc-sys@1.0.0
	rfd@0.11.4
	rle-decode-fast@1.0.3
	ron@0.8.0
	rustc-demangle@0.1.23
	rustc-hash@1.1.0
	rustc_version@0.4.0
	rustdct@0.7.1
	rustfft@6.1.0
	rustix@0.37.20
	rustversion@1.0.12
	ryu@1.0.13
	safe_arch@0.7.0
	same-file@1.0.6
	schannel@0.1.21
	scoped-tls@1.0.1
	scopeguard@1.1.0
	sctk-adwaita@0.5.4
	self_cell@0.10.2
	semver@1.0.17
	serde-wasm-bindgen@0.5.0
	serde-xml-rs@0.6.0
	serde@1.0.164
	serde_derive@1.0.164
	serde_json@1.0.97
	serde_spanned@0.6.2
	sha2@0.10.7
	sharded-slab@0.1.4
	shlex@1.1.0
	simd-adler32@0.3.5
	similar@2.2.1
	simple_asn1@0.6.2
	slab@0.4.8
	slotmap@1.0.6
	sluice@0.5.5
	smallvec@1.10.0
	smithay-client-toolkit@0.16.0
	smithay-clipboard@0.6.6
	snafu-derive@0.7.4
	snafu@0.7.4
	socket2@0.4.9
	spin@0.9.8
	spirv@0.2.0+1.5.4
	sptr@0.3.2
	static_assertions@1.1.0
	str-buf@1.0.6
	strength_reduce@0.2.4
	strict-num@0.1.1
	strsim@0.10.0
	symphonia-bundle-mp3@0.5.3
	symphonia-core@0.5.3
	symphonia-metadata@0.5.3
	symphonia@0.5.3
	syn@1.0.109
	syn@2.0.18
	synstructure@0.13.0
	sys-locale@0.3.0
	system-deps@6.1.0
	target-lexicon@0.12.7
	termcolor@1.2.0
	thiserror-impl@1.0.40
	thiserror@1.0.40
	thread_local@1.1.7
	threadpool@1.8.1
	tiff@0.8.1
	time-core@0.1.1
	time-macros@0.2.9
	time@0.3.22
	tiny-skia-path@0.8.4
	tiny-skia@0.8.4
	tinystr@0.7.1
	tinyvec@1.6.0
	tinyvec_macros@0.1.1
	toml@0.7.4
	toml_datetime@0.6.2
	toml_edit@0.19.10
	tracing-attributes@0.1.24
	tracing-core@0.1.31
	tracing-futures@0.2.5
	tracing-log@0.1.3
	tracing-subscriber@0.3.17
	tracing-tracy@0.10.2
	tracing-wasm@0.2.1
	tracing@0.1.37
	tracy-client-sys@0.21.0
	tracy-client@0.15.2
	transpose@0.2.2
	ttf-parser@0.19.0
	type-map@0.4.0
	type-map@0.5.0
	typed-arena@2.0.2
	typenum@1.16.0
	unic-langid-impl@0.9.1
	unic-langid-macros-impl@0.9.1
	unic-langid-macros@0.9.1
	unic-langid@0.9.1
	unicode-bidi@0.3.13
	unicode-ident@1.0.9
	unicode-normalization@0.1.22
	unicode-segmentation@1.10.1
	unicode-width@0.1.10
	unicode-xid@0.2.4
	url@2.4.0
	utf8parse@0.2.1
	valuable@0.1.0
	vcpkg@0.2.15
	vec_map@0.8.2
	vergen@8.2.1
	version-compare@0.1.1
	version_check@0.9.4
	vswhom-sys@0.1.2
	vswhom@0.1.0
	waker-fn@1.1.0
	walkdir@2.3.3
	wasi@0.11.0+wasi-snapshot-preview1
	wasm-bindgen-backend@0.2.87
	wasm-bindgen-futures@0.4.37
	wasm-bindgen-macro-support@0.2.87
	wasm-bindgen-macro@0.2.87
	wasm-bindgen-shared@0.2.87
	wasm-bindgen@0.2.87
	wayland-client@0.29.5
	wayland-commons@0.29.5
	wayland-cursor@0.29.5
	wayland-protocols@0.29.5
	wayland-scanner@0.29.5
	wayland-sys@0.29.5
	weak-table@0.3.2
	web-sys@0.3.64
	webbrowser@0.8.10
	weezl@0.1.7
	wgpu-core@0.16.1
	wgpu-hal@0.16.1
	wgpu-types@0.16.0
	wgpu@0.16.1
	wide@0.7.10
	widestring@1.0.2
	winapi-i686-pc-windows-gnu@0.4.0
	winapi-util@0.1.5
	winapi-wsapoll@0.1.1
	winapi-x86_64-pc-windows-gnu@0.4.0
	winapi@0.3.9
	windows-sys@0.42.0
	windows-sys@0.45.0
	windows-sys@0.48.0
	windows-targets@0.42.2
	windows-targets@0.48.0
	windows@0.44.0
	windows@0.46.0
	windows@0.48.0
	windows_aarch64_gnullvm@0.42.2
	windows_aarch64_gnullvm@0.48.0
	windows_aarch64_msvc@0.42.2
	windows_aarch64_msvc@0.48.0
	windows_i686_gnu@0.42.2
	windows_i686_gnu@0.48.0
	windows_i686_msvc@0.42.2
	windows_i686_msvc@0.48.0
	windows_x86_64_gnu@0.42.2
	windows_x86_64_gnu@0.48.0
	windows_x86_64_gnullvm@0.42.2
	windows_x86_64_gnullvm@0.48.0
	windows_x86_64_msvc@0.42.2
	windows_x86_64_msvc@0.48.0
	winit@0.28.6
	winnow@0.4.7
	winreg@0.11.0
	x11-dl@2.21.0
	x11rb-protocol@0.10.0
	x11rb@0.10.1
	xcursor@0.3.4
	xml-rs@0.8.14
	yaml-rust@0.4.5
	yansi@0.5.1
"

declare -A GIT_CRATES=(
	[dasp]='https://github.com/RustAudio/dasp;f05a703d247bb504d7e812b51e95f3765d9c5e94;dasp-%commit%/dasp'
	[dasp_envelope]='https://github.com/RustAudio/dasp;f05a703d247bb504d7e812b51e95f3765d9c5e94;dasp-%commit%/dasp_envelope'
	[dasp_frame]='https://github.com/RustAudio/dasp;f05a703d247bb504d7e812b51e95f3765d9c5e94;dasp-%commit%/dasp_frame'
	[dasp_interpolate]='https://github.com/RustAudio/dasp;f05a703d247bb504d7e812b51e95f3765d9c5e94;dasp-%commit%/dasp_interpolate'
	[dasp_peak]='https://github.com/RustAudio/dasp;f05a703d247bb504d7e812b51e95f3765d9c5e94;dasp-%commit%/dasp_peak'
	[dasp_ring_buffer]='https://github.com/RustAudio/dasp;f05a703d247bb504d7e812b51e95f3765d9c5e94;dasp-%commit%/dasp_ring_buffer'
	[dasp_rms]='https://github.com/RustAudio/dasp;f05a703d247bb504d7e812b51e95f3765d9c5e94;dasp-%commit%/dasp_rms'
	[dasp_sample]='https://github.com/RustAudio/dasp;f05a703d247bb504d7e812b51e95f3765d9c5e94;dasp-%commit%/dasp_sample'
	[dasp_signal]='https://github.com/RustAudio/dasp;f05a703d247bb504d7e812b51e95f3765d9c5e94;dasp-%commit%/dasp_signal'
	[dasp_slice]='https://github.com/RustAudio/dasp;f05a703d247bb504d7e812b51e95f3765d9c5e94;dasp-%commit%/dasp_slice'
	[dasp_window]='https://github.com/RustAudio/dasp;f05a703d247bb504d7e812b51e95f3765d9c5e94;dasp-%commit%/dasp_window'
	[flash-lso]='https://github.com/ruffle-rs/rust-flash-lso;8376453eddddbe701031a091c0eed94068fa5649;rust-flash-lso-%commit%/flash-lso'
	[gc-arena-derive]='https://github.com/kyren/gc-arena;63dab12871321e0e5ada10ff1f1de8f4cf1764f9;gc-arena-%commit%/src/gc-arena-derive'
	[gc-arena]='https://github.com/kyren/gc-arena;63dab12871321e0e5ada10ff1f1de8f4cf1764f9;gc-arena-%commit%/src/gc-arena'
	[h263-rs-yuv]='https://github.com/ruffle-rs/h263-rs;d5d78eb251c1ce1f1da57c63db14f0fdc77a4b36;h263-rs-%commit%/yuv'
	[h263-rs]='https://github.com/ruffle-rs/h263-rs;d5d78eb251c1ce1f1da57c63db14f0fdc77a4b36;h263-rs-%commit%/h263'
	[nellymoser-rs]='https://github.com/ruffle-rs/nellymoser;4a33521c29a918950df8ae9fe07e527ac65553f5;nellymoser-%commit%'
	[nihav_codec_support]='https://github.com/ruffle-rs/nihav-vp6;9416fcc9fc8aab8f4681aa9093b42922214abbd3;nihav-vp6-%commit%/nihav-codec-support'
	[nihav_core]='https://github.com/ruffle-rs/nihav-vp6;9416fcc9fc8aab8f4681aa9093b42922214abbd3;nihav-vp6-%commit%/nihav-core'
	[nihav_duck]='https://github.com/ruffle-rs/nihav-vp6;9416fcc9fc8aab8f4681aa9093b42922214abbd3;nihav-vp6-%commit%/nihav-duck'
)

inherit cargo

DESCRIPTION=""
HOMEPAGE="https://ruffle.rs"
SRC_URI="
	${CARGO_CRATE_URIS}
"

LICENSE="|| ( Apache-2.0 MIT )"
# Dependent crate licenses
LICENSE+="
	Apache-2.0 Apache-2.0-with-LLVM-exceptions BSD-2 BSD Boost-1.0
	CC0-1.0 ISC MIT MPL-2.0 OFL-1.1 UbuntuFontLicense-1.0
	Unicode-DFS-2016 ZLIB
"
SLOT="0"
KEYWORDS="~amd64"
