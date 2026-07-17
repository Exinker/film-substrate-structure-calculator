import os
from dataclasses import dataclass
from typing import Sequence

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from calculator import ROOT
from calculator.config import DataKind
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

        y_truncated = np.array(self.y)
        y_truncated[self.y >= __max_value] = np.nan

        return Datum(
            x=np.array(self.x),
            y=y_truncated,
        )

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
            'ref-standard': 'le',
            'flat-standard': 'l0',
            'h': 'h',
        }[kind]

        dat = cls._load(
            filedir=os.path.join(ROOT, 'data', sample_name),
            filename=filename,
        )

        return cls(
            [Datum(x=dat.index, y=dat[column]) for column in dat.columns],
            kind=filename,
        )

    @staticmethod
    def _load(filedir: str, filename: str) -> Frame:

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
