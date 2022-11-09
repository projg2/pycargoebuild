from pycargoebuild.cargo import Crate


CARGO_LOCK_TOML = b'''
    version = 3

    [[package]]
    name = "libc"
    version = "0.2.124"
    source = "registry+https://github.com/rust-lang/crates.io-index"
    checksum = """21a41fed9d98f27ab1c6d161da622a4f\\
                  a35e8a54a8adc24bbf3ddd0ef70b0e50"""

    [[package]]
    name = "fsevent-sys"
    version = "4.1.0"
    source = "registry+https://github.com/rust-lang/crates.io-index"
    checksum = """76ee7a02da4d231650c7cea31349b889\\
                  be2f45ddb3ef3032d2ec8185f6313fd2"""
    dependencies = [
     "libc",
    ]

    [[package]]
    name = "test"
    version = "1.2.3"
    dependencies = [
     "fsevent-sys",
    ]
'''

CRATES = [
    Crate("libc", "0.2.124", "21a41fed9d98f27ab1c6d161da622a4f"
                             "a35e8a54a8adc24bbf3ddd0ef70b0e50"),
    Crate("fsevent-sys", "4.1.0", "76ee7a02da4d231650c7cea31349b889"
                                  "be2f45ddb3ef3032d2ec8185f6313fd2"),
]
