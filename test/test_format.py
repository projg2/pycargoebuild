# pycargoebuild
# (c) 2022-2024 Michał Górny <mgorny@gentoo.org>
# SPDX-License-Identifier: GPL-2.0-or-later

import pytest

from pycargoebuild.format import format_license_var

FORMAT_TESTS = {
    "": "",
    "A": "A",
    "A B C": "A B C",
    "|| ( A B C )": "|| ( A B C )",
    "A B || ( C D )": """
\tA B
\t|| ( C D )
""",
    "A B || ( C D ) E F": """
\tA B
\t|| ( C D )
\tE F
""",
    "|| ( A B ) C D": """
\t|| ( A B )
\tC D
""",
    "A || ( B ( C D ) )": """
\tA
\t|| (
\t\tB
\t\t( C D )
\t)
""",
    "|| ( ( A B ) ( C D ) )": """
\t|| (
\t\t( A B )
\t\t( C D )
\t)
""",
    "A || ( B ( C || ( D E ) ) )": """
\tA
\t|| (
\t\tB
\t\t(
\t\t\tC
\t\t\t|| ( D E )
\t\t)
\t)
""",

    # line wrapping tests
    #    4   8  12  16  20  24
    # LICENSE="ABCD ABCD ABCD"
    # tab>ABCD ABCD ABCD ABCD
    "ABCD ABCD ABCD": "ABCD ABCD ABCD",
    "ABCD ABCD ABCD ABCD": """
\tABCD ABCD ABCD ABCD
""",
    "ABCD ABCD ABCD ABCD ABCD": """
\tABCD ABCD ABCD ABCD
\tABCD
""",
    "ABCD ABCD ABCD ABCD ABCD || ( ABC ABC ABC )": """
\tABCD ABCD ABCD ABCD
\tABCD
\t|| ( ABC ABC ABC )
""",
    "ABCD ABCD ABCD ABCD ABCD || ( ABCD ABCD ABCD )": """
\tABCD ABCD ABCD ABCD
\tABCD
\t|| (
\t\tABCD ABCD ABCD
\t)
""",
    "ABCD ABCD ABCD ABCD ABCD || ( ABCD ABCD ABCD ABCD )": """
\tABCD ABCD ABCD ABCD
\tABCD
\t|| (
\t\tABCD ABCD ABCD
\t\tABCD
\t)
""",
}


@pytest.mark.parametrize("value", FORMAT_TESTS)
def test_format_license_var(value):
    assert format_license_var(value, prefix='LICENSE="', line_width=24
                              ) == FORMAT_TESTS[value]
