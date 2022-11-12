import configparser
import importlib.resources
import sys
import typing

import license_expression


MAPPING: typing.Dict[str, str] = {}


def load_license_mapping() -> None:
    conf = configparser.ConfigParser(comment_prefixes=("#",),
                                     delimiters=("=",),
                                     empty_lines_in_values=False,
                                     interpolation=None)

    if sys.version_info >= (3, 9):
        f = ((importlib.resources.files(__package__) / "license-mapping.conf")
             .open("r"))

    else:
        f = importlib.resources.open_text(__package__, "license-mapping.conf")

    with f:
        conf.read_file(f)

    MAPPING.update((k.lower(), v) for k, v in conf.items("spdx-to-ebuild"))


def symbol_to_ebuild(license_symbol: license_expression.LicenseSymbol) -> str:
    return MAPPING[str(license_symbol).lower()]


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
            yield "|| ("
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
