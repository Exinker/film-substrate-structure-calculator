import pytest

from calculator.config import DETECTOR_PITCH
from calculator.types import N


@pytest.fixture
def expected(
    n_numbers: int,
    delta: N,
) -> N:

    left, right = [1/4*n_numbers - delta/2, 3/4*n_numbers + delta/2]
    return DETECTOR_PITCH*(right - left)
