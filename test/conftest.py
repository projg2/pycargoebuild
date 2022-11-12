import pytest

from pycargoebuild.license import load_license_mapping


@pytest.fixture
def real_license_mapping() -> None:
    load_license_mapping()
