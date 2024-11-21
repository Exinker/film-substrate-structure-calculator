import os
from dataclasses import dataclass
from typing import Sequence

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from calculator.config import DataKind, VERSION
from calculator.data.utils import calculate_cursor
from calculator.types import Array, Frame, N, SampleName, U


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
        cursor = cursor or calculate_cursor(
            x=self.x,
            y=self.y,
            kind='center mass',
        )

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

    def __new__(cls, __data: Sequence[Datum], *args, **kwargs):
        return super().__new__(cls, __data)

    def __init__(self, __data: Sequence[Datum], kind: DataKind):
        self.kind = kind

    @classmethod
    def load(cls, sample_name: SampleName, kind: DataKind) -> 'Data':
        filename = {
            'sample': sample_name,
            'ref-standard': 'Iэт',
            'flat-standard': 'I0',
            'h': 'h',
        }.get(kind, None)

        dat = cls._load(
            filedir=os.path.join(os.getcwd(), 'data', sample_name),
            filename=filename,
        )

        return cls(
            [Datum(x=dat.index, y=dat[column]) for column in dat.columns],
            kind=filename,
        )

    @staticmethod
    def _load(filedir: str, filename: str) -> Frame:

        if VERSION == '0.1':
            filepath = os.path.join(filedir, f'{filename}.xlsx')

            dat = pd.read_excel(
                filepath,
                header=None,
                index_col=0,
                engine='openpyxl',
            )
            return dat

        if VERSION == '0.2':

            data = []
            for _ in os.listdir(os.path.join(filedir, f'{filename}')):

                filepath = os.path.join(filedir, f'{filename}', _)
                with open(filepath, 'r') as file:
                    datum = pd.read_csv(
                        file,
                        names=['wavelength', 'intensity', 'crystal', 'clipped'],
                        sep=r'\t',
                        engine='python',
                    )

                    data.append(tuple(datum['intensity']))

            dat = pd.DataFrame(np.array(data).T)
            return dat

        raise ValueError(f'Version {VERSION} is not supported yet!')
