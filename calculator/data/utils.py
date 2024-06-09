import numpy as np

from calculator.types import Array, N, U


def calculate_cursor(x: Array[N], y: Array[U]) -> int:
    index = ~np.isnan(y)

    return np.round(np.dot(x[index], y[index]) / np.sum(y[index])).astype(int)
