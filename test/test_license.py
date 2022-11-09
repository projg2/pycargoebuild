import unittest.mock

import license_expression
import pytest

from pycargoebuild.license import spdx_to_ebuild

TEST_LICENSE_MAPPING = {
    "A": "A",
    "B": "B",
    "C": "Cm",
    "A WITH EXC": "A-EXC",
    "B WITH EXC": "B-EXC",
}

SPDX_TEST_SYMBOLS = [
    "A",
    "B",
    "C",
    license_expression.LicenseSymbol("EXC", is_exception=True),
]

SPDX_TEST_VALUES = {
    "A": "A",
    "B": "B",
    "C": "Cm",
    "A AND B": "A B",
    "A AND B AND C": "A B Cm",
    "A OR B": "|| ( A B )",
    "A OR B OR C": "|| ( A B Cm )",
    "A AND ( B OR C )": "A || ( B Cm )",
    "( A AND B ) OR C": "|| ( ( A B ) Cm )",
    "A AND B OR C": "|| ( ( A B ) Cm )",
    "A AND B OR C AND B": "|| ( ( A B ) ( Cm B ) )",
    "A WITH EXC": "A-EXC",
    "A WITH EXC AND B": "A-EXC B",
    "A WITH EXC OR B": "|| ( A-EXC B )",
    "A AND B WITH EXC": "A B-EXC",
    "A OR B WITH EXC": "|| ( A B-EXC )",
}


@pytest.fixture(scope="module")
def spdx() -> license_expression.Licensing:
    with unittest.mock.patch("pycargoebuild.license.MAPPING",
                             new=TEST_LICENSE_MAPPING):
        yield license_expression.Licensing(SPDX_TEST_SYMBOLS)


@pytest.mark.parametrize("value", SPDX_TEST_VALUES)
def test_spdx_to_ebuild(spdx, value):
    parsed_license = spdx.parse(value, validate=True, strict=True)
    assert spdx_to_ebuild(parsed_license) == SPDX_TEST_VALUES[value]
