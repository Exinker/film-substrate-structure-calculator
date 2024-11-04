from functools import partial

import matplotlib.pyplot as plt
import numpy as np
from scipy import optimize

from calculator.data import Datum
from calculator.data.utils import calculate_cursor
from calculator.types import Array, N, U


def gauss(
    x: Array[N],
    position: N,
    width: N,
    intensity: U,
) -> Array[U]:
    """Gauss (or normal) distribution with given `position` and `intensity`."""

    f = intensity * np.exp(-(1/2)*((x - position) / width)**2) / (np.sqrt(2*np.pi) * width)

    return f


def approximate(datum: Datum, show: bool = False) -> N:
    """Approximate `datum` by `gauss` shape."""

    def loss(x: Array[N], y: Array[U], params) -> float:
        y_hat = gauss(x, *params[:3]) + params[3]

        return np.sqrt(np.nansum((y - y_hat)**2))

    res = optimize.minimize(
        partial(loss, datum.x, datum.y),
        x0=[
            calculate_cursor(
                x=datum.x,
                y=datum.y,
                kind='maximum',
            ),
            20,
            np.nansum(datum.y - np.nanmedian(datum.y)),
            np.nanmedian(datum.y),
        ],
    )
    # assert res['success'], 'Optimization is not succeeded!'

    if show:
        plt.plot(
            datum.x, datum.y,
            color='black', linestyle='-', linewidth=1, marker='.',
        )
        plt.axvline(
            res['x'][0],
            color='red', linestyle='--', linewidth=1,
        )
        plt.plot(
            datum.x, gauss(datum.x, *res['x'][:3]) + res['x'][3],
            color='red', linestyle='-', linewidth=1,
        )
        plt.text(
            0.05, 0.95,
            '' if res['success'] else 'Optimization is not succeeded!',
            transform=plt.gca().transAxes,
            ha='left', va='top',
        )

    return res['x'][0]
