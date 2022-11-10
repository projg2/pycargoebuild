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
    "ABCD ABCD ABCD": "ABCD ABCD ABCD",
}

@pytest.mark.parametrize("value", FORMAT_TESTS)
def test_format_license_var(value):
    assert format_license_var(value, 'LICENSE="', 24) == FORMAT_TESTS[value]
