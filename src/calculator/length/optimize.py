import warnings
from functools import partial

import numpy as np
from scipy.optimize import OptimizeResult, minimize

from spectrumlab.peaks.blink_peaks import BlinkPeak

from calculator.config import PLUGIN_CONFIG
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


def estimate_amplitude(
    datum: Datum,
    peak: BlinkPeak,
) -> U:

    x = datum.x[peak.number[peak.tail]]
    y = datum.y[peak.number[peak.tail]]

    x0 = np.mean(peak.maxima)
    g = gauss(x, x0, PLUGIN_CONFIG.smooth_window, 1)

    amplitude = np.dot(y, g) / np.dot(g, g)
    return amplitude


def optimize(
    datum: Datum,
    peak: BlinkPeak,
) -> OptimizeResult:

    def loss(x: Array[N], y: Array[U], params) -> float:
        y_hat = gauss(x, *params[:3]) + params[3]

        return np.sqrt(np.nansum((y - y_hat)**2))

    position = np.mean(peak.maxima)
    amplitude = estimate_amplitude(
        datum=datum,
        peak=peak,
    )
    result = minimize(
        partial(loss, datum.x[peak.number], datum.y[peak.number]),
        x0=[
            position,
            PLUGIN_CONFIG.smooth_window,
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

    return result
