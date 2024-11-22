import numpy as np
import pytest

from calculator.config import DETECTOR_PITCH
from calculator.data import Datum
from calculator.length import kernel, gauss
from calculator.types import N, U


def emulate_datum(params: tuple[tuple[N, N, U], tuple[N, N, U]], n: int = 2048) -> Datum:

    x = np.arange(n)
    y = np.zeros(n)
    for position, width, intensity in params:
        y += gauss(x, position=position, width=width, intensity=intensity)
    y[y >= 100] = np.nan

    return Datum(x=x, y=y)


@pytest.mark.parametrize(
    'width', [10, 20, 40, 80],
)
@pytest.mark.parametrize(
    'intensity', [100, 500, 1_000, 10_000],
)
def test_kernel(width: N, intensity: U):
    positions = [1/4*2580, 3/4*2580]
    datum = emulate_datum(
        params=tuple(
            (position, width, intensity)
            for position in positions
        ),
    )

    length_hat = kernel(datum=datum)
    length = DETECTOR_PITCH * (max(positions) - min(positions))

    assert np.isclose(length_hat, length, atol=1e-9)
