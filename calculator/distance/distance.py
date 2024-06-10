import os
from functools import partial
from dataclasses import dataclass

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from calculator.config import PITCH, THRESHOLD
from calculator.data import Data, Datum
from calculator.stats import Stats
from calculator.types import Array, FileDir, Inch, MicroMeter

from .optimize import approximate


@dataclass(frozen=True, slots=True)
class Distance:
    value: MicroMeter | Array[MicroMeter]
    filedir: FileDir

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

    def save(self) -> None:

        filepath = os.path.join(self.filedir, 'distance.xlsx')
        with pd.ExcelWriter(filepath, mode='w', engine='openpyxl') as writer:
            pd.DataFrame({
                'l, мкм': self.value,
            }).to_excel(
                writer,
                index=False,
            )

    @classmethod
    def calculate(cls, data: Data, save: bool = False, show: bool = False, verbose: bool = False) -> 'Distance':
        handler = partial(kernel, show=show, verbose=verbose)
        value = np.array([handler(datum=datum.truncate(THRESHOLD)) for datum in data])

        if save:
            raise NotImplementedError

        return cls(
            value=value,
            filedir=data.filedir,
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
