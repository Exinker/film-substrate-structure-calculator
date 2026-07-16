import random

import numpy as np
import pytest

from spectrumlab.detectors import Detector
from spectrumlab.spectra import EmittedSpectrum as Spectrum

from calculator.data import Data, Datum
from calculator.types import N, U
from tests.utils import emulate_spectrum


@pytest.fixture
def delta(request) -> N:

    return getattr(request, 'param', random.random())


@pytest.fixture(params=np.linspace(10, 100, 6))
def width(request) -> N:

    return request.param


@pytest.fixture(params=np.power(2, np.arange(2, 13)), ids=str)
def amplitude(request) -> U:

    return request.param


@pytest.fixture
def background(request) -> U:

    return getattr(request, 'param', 0)


@pytest.fixture()
def detector(request) -> Detector:

    return getattr(request, 'param', Detector.BLPP369M1)


@pytest.fixture()
def n_numbers() -> int:

    return 2580


@pytest.fixture()
def n_frames(request) -> int:

    return getattr(request, 'param', 100)


@pytest.fixture
def spectrum(
    delta: N,
    width: N,
    amplitude: U,
    background: U,
    detector: Detector,
    n_numbers: int,
    n_frames: int,
) -> Spectrum:

    spectrum = emulate_spectrum(
        delta=delta,
        width=width,
        amplitude=amplitude,
        background=background,
        detector=detector,
        n_numbers=n_numbers,
        n_frames=n_frames,
    )
    return spectrum


@pytest.fixture
def data(
    spectrum: Spectrum,
) -> Data:

    return Data(
        [
            Datum(x=spectrum.index, y=spectrum.intensity),
        ],
        kind='test',
    )
