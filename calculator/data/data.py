import os
from dataclasses import dataclass
from typing import Sequence

import matplotlib.pyplot as plt
import numpy as np

from calculator.types import Array, N, U

from .utils import calculate_cursor


@dataclass(frozen=True, slots=True)
class Datum:
    x: Array[N]
    y: Array[U]

    def show(self) -> None:

        plt.plot(
            self.x, self.y,
            color='black', linestyle='-', linewidth=1,
        )
        plt.show()

    def truncate(self, __max_value: U) -> 'Datum':
        x, y = self.x.copy(), self.y.copy()

        mask = y >= __max_value
        y[mask] = np.nan

        return Datum(x=x, y=y)

    def split(self, cursor: int | None = None) -> tuple['Datum', 'Datum']:
        cursor = cursor or calculate_cursor(x=self.x, y=self.y)

        return self[:cursor], self[cursor:]

    def __getitem__(self, index: slice) -> 'Datum':
        cls = self.__class__

        if isinstance(index, slice):
            return cls(
                x=self.x[index],
                y=self.y[index],
            )

        raise NotImplementedError(f'Slice by {type(index)} if not supported yet!')


class Data(tuple):

    @classmethod
    def load(cls, filedir: str) -> 'Data':

        with open(os.path.join(filedir, 'data.csv'), 'r') as file:
            dat = np.loadtxt(file)

        return cls(
            [Datum(x=dat[:, 0], y=dat[:, i]) for i in range(1, dat.shape[1])],
        )

    def __new__(cls, __data: Sequence[Datum]):
        return super().__new__(cls, __data)
