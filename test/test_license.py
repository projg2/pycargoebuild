import typing
import unittest.mock

import license_expression
import pytest

from pycargoebuild.license import (load_license_mapping,
                                   spdx_to_ebuild,
                                   symbol_to_ebuild,
                                   )

TEST_LICENSE_MAPPING = {
    # keys are lowercase in MAPPING
    "a": "A",
    "b": "B",
    "c": "Cm",
    "a with exc": "A-EXC",
    "b with exc": "B-EXC",
}

SPDX_TEST_SYMBOLS = [
    "A",
    "B",
    "C",
    "A+",
    "MULTI",
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

REAL_MAPPING_TEST_VALUES = {
    "BSD-3-Clause": "BSD",
    "Apache-2.0": "Apache-2.0",
    "aPACHE-2.0": "Apache-2.0",
    "Apache-2.0 WITH LLVM-exception": "Apache-2.0-with-LLVM-exceptions",
    "aPACHE-2.0 WITH llvm-Exception": "Apache-2.0-with-LLVM-exceptions",
}


@pytest.fixture(scope="module")
def spdx() -> typing.Generator[license_expression.Licensing, None, None]:
    with unittest.mock.patch("pycargoebuild.license.MAPPING",
                             new=TEST_LICENSE_MAPPING):
        yield license_expression.Licensing(SPDX_TEST_SYMBOLS)


@pytest.mark.parametrize("value", SPDX_TEST_VALUES)
def test_spdx_to_ebuild(spdx, value):
    parsed_license = spdx.parse(value, validate=True, strict=True)
    assert spdx_to_ebuild(parsed_license) == SPDX_TEST_VALUES[value]


@pytest.fixture(scope="module")
def real_mapping() -> typing.Generator[None, None, None]:
    load_license_mapping()
    yield


@pytest.mark.parametrize("value", REAL_MAPPING_TEST_VALUES)
def test_real_license_mapping(real_mapping, value):
    assert symbol_to_ebuild(value) == REAL_MAPPING_TEST_VALUES[value]
