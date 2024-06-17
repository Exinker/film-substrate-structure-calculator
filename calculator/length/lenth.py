from dataclasses import dataclass
from functools import partial
from typing import Mapping, get_args

import matplotlib.pyplot as plt
import numpy as np

from calculator.config import PITCH, THRESHOLD
from calculator.data import Data, Datum
from calculator.stats import Stats
from calculator.types import Array, Inch, Kind, MicroMeter, SampleName

from .optimize import approximate


class LengthMap(dict):

    def __new__(cls, __data: Mapping[Kind, 'Length'], *args, **kwargs):
        return super().__new__(cls, __data)

    @classmethod
    def calculate(cls, sample_name: SampleName) -> 'LengthMap':

        return cls({
            kind: Length.calculate(data=Data.load(sample_name=sample_name, kind=kind))
            for kind in get_args(Kind)
        })


@dataclass(frozen=True, slots=True)
class Length:
    value: MicroMeter | Array[MicroMeter]

    @property
    def stats(self) -> Stats:
        return Stats.calculate(self.value)

    def show(self, figsize: tuple[Inch, Inch] | None = None, info: bool = False) -> None:
        figsize = figsize or (6, 4)

        fig, ax = plt.subplots(figsize=figsize, tight_layout=True)

        plt.plot(
            self.value,
            color='black', linestyle='-', linewidth=1, marker='.', markersize=2,
        )

        if info:

            # add stats
            stats = self.stats

            plt.text(
                .05, .9,
                f'$l = {stats}$, мкм',
                transform=ax.transAxes,
            )
            plt.axhline(
                stats.value,
                color='grey', linestyle='--', linewidth=1,
            )
            plt.axhspan(
                stats.value - stats.interval,
                stats.value + stats.interval,
                color='grey',
                alpha=.1,
            )

        plt.xlabel('Номер измерения')
        plt.ylabel('Расстояние, мкм')

        plt.show()

    @classmethod
    def calculate(cls, data: Data, save: bool = False, show: bool = False, verbose: bool = False) -> 'Length':
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
    length = pitch * (max(positions) - min(positions))

    if show:
        plt.show()

    return length
