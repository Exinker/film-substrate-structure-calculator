from dataclasses import dataclass
from functools import partial
from typing import Mapping, get_args

import matplotlib.pyplot as plt
import numpy as np
from tqdm.notebook import tqdm

from calculator.config import DataKind, DETECTOR_PITCH, DETECTOR_THRESHOLD
from calculator.data import Data, Datum
from calculator.length.optimize import approximate
from calculator.stats import Stats
from calculator.types import Array, Inch, MicroMeter, SampleName


class LengthMap(dict):

    def __new__(
        cls,
        __data: Mapping[DataKind, 'Length'],
        *args,
        **kwargs,
    ):
        return super().__new__(cls, __data)

    @classmethod
    def calculate(
        cls,
        sample_name: SampleName,
        verbose: bool = False,
    ) -> 'LengthMap':

        return cls({
            kind: Length.calculate(
                data=Data.load(
                    sample_name=sample_name,
                    kind=kind,
                ),
                verbose=verbose,
            )
            for kind in get_args(DataKind)
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
    def calculate(
        cls,
        data: Data,
        show: bool = False,
        verbose: bool = False,
    ) -> 'Length':
        handler = partial(kernel, show=show)
        value = np.array([
            handler(
                datum=datum.truncate(DETECTOR_THRESHOLD),
            )
            for datum in tqdm(data, desc=f'{data.kind:<15}', disable=not verbose)
        ])

        return cls(
            value=value,
        )

    def __str__(self) -> str:
        return '[{}]'.format(
            '; '.join(map(str, self.value)),
        )


def kernel(
    datum: Datum,
    pitch: MicroMeter = DETECTOR_PITCH,
    show: bool = False,
) -> MicroMeter:
    left, right = datum.split()

    positions = approximate(datum=left, show=show), approximate(datum=right, show=show)
    length = pitch * (max(positions) - min(positions))

    if show:
        plt.show()

    return length
