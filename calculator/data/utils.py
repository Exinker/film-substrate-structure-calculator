from typing import Literal

import numpy as np

from calculator.types import Array, N, U


Kind = Literal['maximum', 'center mass']


def calculate_cursor(x: Array[N], y: Array[U], kind: Kind = 'maximum') -> int:

    if kind == 'maximum':
        if np.any(np.isnan(y)):
            # В случае, если есть зашкаленные отсчеты, то берется серединка зашкала.
            index = np.mean(np.argwhere(np.isnan(y)), dtype=int)
            return x[index]
        return x[np.argmax(y)]

    if kind == 'center mass':
        index = ~np.isnan(y)
        return np.round(np.dot(x[index], y[index]) / np.sum(y[index])).astype(int)

    raise ValueError(f'Kind {kind} is not supported yet!')
