import os
from dataclasses import dataclass
from typing import Literal, Sequence

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from calculator.types import Array, FileDir, N, U

from .utils import calculate_cursor


Kind = Literal['sample', 'standard', 'flat']


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
    def load(cls, name: str, kind: Kind) -> 'Data':

        filedir = os.path.join(os.getcwd(), 'data', name)
        filename = {
            'sample': 'data',
        }.get(kind, kind)
        filepath = os.path.join(filedir, f'{filename}.xlsx')

        dat = pd.read_excel(
            filepath,
            header=None,
            index_col=0,
            engine='openpyxl',
        )

        return cls(
            [Datum(x=dat.index, y=dat[column]) for column in dat.columns],
            filedir=filedir,
            kind=kind,
        )

    def __new__(cls, __data: Sequence[Datum], *args, **kwargs):
        return super().__new__(cls, __data)

    def __init__(self, __data: Sequence[Datum], filedir: FileDir, kind: Kind):
        self.filedir = filedir
        self.kind = kind
