import numpy as np
import pytest

from calculator.data import Data
from calculator.length import Length
from calculator.types import N


@pytest.mark.parametrize(
    'delta', np.linspace(0, 1, 11), ids=str, indirect=True,
)
def test_calculate(
    data: Data,
    expected: N,
):

    length = Length.calculate(
        data=data,
    )

    assert np.isclose(length.value, expected, rtol=1e-2)


@pytest.mark.parametrize(
    'delta', [0, 1], ids=str, indirect=True,
)
@pytest.mark.parametrize(
    'amplitude', np.power(2, np.arange(13, 21)), ids=str,
)
def test_calculate_with_high_clipping(
    data: Data,
    expected: N,
):

    length = Length.calculate(
        data=data,
    )

    assert np.isclose(length.value, expected, rtol=1e-2)



@pytest.mark.parametrize(
    'background', [-0.42, ],
)
@pytest.mark.parametrize(
    'width', [20, ],
)
@pytest.mark.parametrize(
    'amplitude', [100, ],
)
def test_calculate_with_negative_background(
    data: Data,
    expected: N,
):

    length = Length.calculate(
        data=data,
    )

    assert np.isclose(length.value, expected, rtol=1e-2)
