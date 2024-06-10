import numpy as np
import pytest

from calculator.config import PITCH
from calculator.data import Datum
from calculator.distance import kernel, gauss
from calculator.types import N, U


def emulate_datum(params: tuple[tuple[N, N, U], tuple[N, N, U]], n: int = 2048) -> Datum:

    x = np.arange(n)

    y = np.zeros(n)
    for position, width, intensity in params:
        y += gauss(x, position=position, width=width, intensity=intensity)
    y[y >= 100] = np.nan

    return Datum(x=x, y=y)


@pytest.mark.parametrize(
    'params',
    [
        ((700, 10, 20_000), (1700, 10, 10_000)),
        ((700, 20, 20_000), (1700, 20, 10_000)),
        ((700, 40, 20_000), (1700, 40, 10_000)),
    ],
)
def test__calculate(params: tuple[tuple[N, N, U], tuple[N, N, U]]):
    positions = [position for position, *_ in params]

    datum = emulate_datum(params=params)

    distance = PITCH * (max(positions) - min(positions))
    distance_hat = kernel(datum=datum)

    assert np.isclose(distance, distance_hat, atol=1e-9)
