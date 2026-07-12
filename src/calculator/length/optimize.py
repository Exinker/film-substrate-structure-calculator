import warnings
from functools import partial

import numpy as np
from scipy.optimize import OptimizeResult, minimize

from spectrumlab.peaks.blink_peaks import BlinkPeak

from calculator.config import SMOOTH_WINDOW as WIDTH
from calculator.data import Datum
from calculator.types import Array, N, U

warnings.filterwarnings('ignore', category=RuntimeWarning)


def gauss(
    x: Array[N],
    x0: N,
    width: N,
    amplitude: U,
) -> Array[U]:

    f = amplitude * np.exp(-(1/2)*((x - x0) / width)**2)
    return f


def estimate_position(
    datum: Datum,
    peak: BlinkPeak,
) -> N:

    index = np.isnan(datum.y[peak.number])
    if np.any(index) and np.sum(index) > 5:
        number = peak.number[index]
        return int(np.round(np.mean(number)))

    return peak.maxima[0]


def estimate_amplitude(
    datum: Datum,
    peak: BlinkPeak,
    position: N,
) -> U:

    index = np.isfinite(datum.y[peak.number])
    number = peak.number[index]
    x = datum.x[number]
    y = datum.y[number]

    x0 = position
    g = gauss(x, x0, WIDTH, 1)

    integral = np.dot(y, g) / np.dot(g, g)

    amplitude = integral / (np.sqrt(2*np.pi) * WIDTH)
    return amplitude


def optimize(
    datum: Datum,
    peak: BlinkPeak,
) -> OptimizeResult:

    def loss(x: Array[N], y: Array[U], params) -> float:
        y_hat = gauss(x, *params[:3]) + params[3]

        return np.sqrt(np.nansum((y - y_hat)**2))

    position = estimate_position(
        datum=datum,
        peak=peak,
    )
    amplitude = estimate_amplitude(
        datum=datum,
        peak=peak,
        position=position,
    )
    res = minimize(
        partial(loss, datum.x[peak.number], datum.y[peak.number]),
        x0=[
            position,
            WIDTH,
            amplitude,
            np.nanpercentile(datum.y, 50),
        ],
        bounds=[
            (position-100, position+100),
            (10, None),
            (0, None),
            (np.nanpercentile(datum.y, 0), np.nanpercentile(datum.y, 50)),
        ],
    )
    # assert res['success'], 'Optimization is not succeeded!'

    return res
