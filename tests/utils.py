import numpy as np

from spectrumlab.detectors import Detector
from spectrumlab.noises import EmittedSpectrumNoise
from spectrumlab.spectra import EmittedSpectrum

from calculator.length import gauss
from calculator.types import N, U

INTENSITY_MAX = 100


def emulate_spectrum(
    delta: N,
    width: N,
    amplitude: U,
    background: U,
    detector: Detector,
    n_numbers: int,
    n_frames: int,
    is_noised: bool = True,
    is_clipped: bool = True,
) -> EmittedSpectrum:

    noise = EmittedSpectrumNoise(
        detector=detector,
        n_frames=n_frames,
    )

    positions = np.array([1/4*n_numbers, 3/4*n_numbers]) + np.array([-delta/2, +delta/2])

    x = np.arange(n_numbers)
    intensity = np.zeros(n_numbers)
    intensity += background
    for position in positions:
        intensity += gauss(x, x0=position, width=width, amplitude=amplitude)

    if is_noised:
        intensity += noise(intensity)*np.random.randn(n_numbers)  # add noise

    if is_clipped:
        intensity[intensity > INTENSITY_MAX] = INTENSITY_MAX

    return EmittedSpectrum(
        intensity=intensity,
        clipped=intensity==INTENSITY_MAX,
    )
