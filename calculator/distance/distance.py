from functools import partial
from dataclasses import dataclass

import matplotlib.pyplot as plt
import numpy as np

from calculator.config import PITCH, THRESHOLD
from calculator.data import Data, Datum
from calculator.stats import Stats
from calculator.types import Array, MicroMeter

from .optimize import approximate


@dataclass(frozen=True, slots=True)
class Distance:
    value: MicroMeter | Array[MicroMeter]

    @property
    def stats(self) -> Stats:
        return Stats.calculate(self.value)

    @classmethod
    def calculate(cls, data: Data, save: bool = False, show: bool = False, verbose: bool = False) -> 'Distance':
        handler = partial(kernel, show=show, verbose=verbose)
        value = np.array([handler(datum=datum.truncate(THRESHOLD)) for datum in data])

        if save:
            raise NotImplementedError

        return cls(
            value=value,
        )

    def __str__(self) -> str:
        return '[{}]'.format(
            '; '.join(map(str, self.value)),
        )


def kernel(datum: Datum, pitch: MicroMeter = PITCH, show: bool = False, verbose: bool = False) -> MicroMeter:
    left, right = datum.split()

    positions = approximate(datum=left, show=show, verbose=verbose), approximate(datum=right, show=show, verbose=verbose)
    distance = pitch * (max(positions) - min(positions))

    if show:
        plt.show()

    return distance
