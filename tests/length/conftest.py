import pytest

from calculator.config import PLUGIN_CONFIG
from calculator.types import N


@pytest.fixture
def expected(
    n_numbers: int,
    delta: N,
) -> N:

    left, right = [1/4*n_numbers - delta/2, 3/4*n_numbers + delta/2]
    return PLUGIN_CONFIG.detector_pitch*(right - left)
