# pycargoebuild
# (c) 2022-2024 Michał Górny <mgorny@gentoo.org>
# SPDX-License-Identifier: GPL-2.0-or-later

import io

import pytest

from pycargoebuild.license import load_license_mapping

TEST_LICENSE_MAPPING_CONF = """
[spdx-to-ebuild]
Apache-2.0 = Apache-2.0
Apache-2.0 WITH LLVM-exception = Apache-2.0-with-LLVM-exceptions
BSD-3-Clause = BSD
CC0-1.0 = CC0-1.0
MIT = MIT
Unicode-DFS-2016 = Unicode-DFS-2016
Unlicense = Unlicense
"""


@pytest.fixture
def real_license_mapping() -> None:
    with io.StringIO(TEST_LICENSE_MAPPING_CONF) as f:
        load_license_mapping(f)
