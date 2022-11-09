import typing

import license_expression


MAPPING = {
    "Apache-2.0": "Apache-2.0",
    "Apache-2.0 WITH LLVM-exception": "Apache-2.0-with-LLVM-exceptions",
    "ISC": "ISC",
    "MIT": "MIT",
    "Artistic-2.0": "Artistic-2",
    "CC0-1.0": "CC0-1.0",
    "Unlicense": "Unlicense",
}


def symbol_to_ebuild(license_symbol: license_expression.LicenseSymbol) -> str:
    return MAPPING[str(license_symbol)]


def spdx_to_ebuild(spdx: license_expression.Renderable) -> str:
    """
    Convert SPDX license expression to ebuild license string.
    """
    def sub(x: license_expression.LicenseExpression, top: bool = False
            ) -> typing.Generator[str, None, None]:
        if isinstance(x, license_expression.AND):
            if not top:
                yield "("
            for y in x.args:
                yield from sub(y)
            if not top:
                yield ")"
        elif isinstance(x, license_expression.OR):
            yield "||"
            yield "("
            for y in x.args:
                yield from sub(y)
            yield ")"
        elif isinstance(x, license_expression.LicenseSymbol):
            yield symbol_to_ebuild(x)
        elif isinstance(x, license_expression.LicenseWithExceptionSymbol):
            yield symbol_to_ebuild(x)
        else:
            assert False, f"Unknown type {type(x)}"

    return " ".join(sub(spdx, top=True))
