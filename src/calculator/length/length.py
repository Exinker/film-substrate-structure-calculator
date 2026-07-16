from collections.abc import Sequence
from dataclasses import dataclass
from typing import Mapping, get_args

import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
from tqdm.notebook import tqdm

from spectrumlab.peaks.blink_peaks import (
    BlinkPeak,
    DraftBlinksConfig,
    draft_blinks,
)
from spectrumlab.spectra import EmittedSpectrum as Spectrum

from calculator.config import (
    DETECTOR_PITCH,
    THRESHOLD,
    SMOOTH_WINDOW,
    DataKind,
)
from calculator.data import Data, Datum
from calculator.length.optimize import optimize, gauss
from calculator.stats import Stats
from calculator.types import Array, Inch, MicroMeter, N, SampleName, U


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
        show: bool = False,
    ) -> 'LengthMap':

        return cls({
            kind: Length.calculate(
                data=Data.load(
                    sample_name=sample_name,
                    kind=kind,
                ),
                show=show,
            )
            for kind in get_args(DataKind)
        })


@dataclass(frozen=True, slots=True)
class Length:
    value: MicroMeter | Array[MicroMeter]

    @property
    def stats(self) -> Stats:
        return Stats.calculate(self.value)

    def show(
        self,
        figsize: tuple[Inch, Inch] | None = None,
        info: bool = False,
    ) -> None:
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
    ) -> 'Length':

        value = np.array([
            kernel(
                datum=datum.truncate(THRESHOLD),
                show=show,
            )
            for datum in tqdm(data, desc=f'{data.kind:<15}')
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

    peaks = find_peaks(
        datum=datum,
        window=SMOOTH_WINDOW,
        show=show,
    )

    results = [
        optimize(
            datum=datum,
            peak=peak,
        )
        for peak in peaks
    ]
    positions = [result['x'][0] for result in results]
    length = pitch * (max(positions) - min(positions))

    if show:
        remainder = datum.y

        fig, (ax_left, ax_right) = plt.subplots(ncols=2, figsize=(12, 4))

        plt.sca(ax_left)
        plt.plot(
            datum.x, datum.y,
            color='black', linestyle='none', marker='.',
        )
        for i, (peak, result) in enumerate(zip(peaks, results)):
            plt.plot(
                peak.number, gauss(peak.number, *result['x'][:3]) + result['x'][3],
                color='red', linestyle='-', linewidth=1,
            )
            plt.axvline(
                result['x'][0],
                color='red', linestyle='--', linewidth=1,
            )
            plt.axvspan(
                *peak.minima,
                color='red', alpha=.1,
            )
            text = '\n'.join([
                '' if result['success'] else 'Optimization is not succeeded!',
                '$x_{{0}}$: {:.2f}'.format(result['x'][0]),
                '$w$: {:.2f}'.format(result['x'][1]),
                '$A$: {:.2f}'.format(result['x'][2]),
                '$b$: {:.4f}'.format(result['x'][3]),
            ])
            if i == 0:
                plt.text(
                    0.025, 0.975,
                    text,
                    transform=plt.gca().transAxes,
                    ha='left', va='top',
                )
            else:
                plt.text(
                    0.975, 0.975,
                    text,
                    transform=plt.gca().transAxes,
                    ha='right', va='top',
                )

            remainder[peak.number] -= gauss(peak.number, *result['x'][:3])

        plt.xlabel('Номер отсчета')
        plt.ylabel(r'$I$, %')
        plt.grid(color='grey', linestyle=':')

        plt.sca(ax_right)
        plt.plot(
            datum.x, remainder,
            color='black', linestyle='none', marker='.',
        )
        for i, (peak, result) in enumerate(zip(peaks, results)):
            plt.axvline(
                result['x'][0],
                color='red', linestyle='--', linewidth=1,
            )
            plt.axvspan(
                *peak.minima,
                color='red', alpha=.1,
            )
        plt.xlabel('Номер отсчета')
        plt.ylabel(r'$I$, %')
        plt.grid(color='grey', linestyle=':')

        plt.show()

    return length


def find_peaks(
    datum: Datum,
    window: int,
    show: bool = False,
) -> Sequence[BlinkPeak]:

    spectrum = Spectrum(
        number=datum.x,
        intensity=smooth_intensity(
            x=datum.x,
            y=datum.y,
            window=window,
        ),
        clipped=np.isnan(datum.y),
    )

    blinks = draft_blinks(
        spectrum=spectrum,
        config=DraftBlinksConfig(
            n_counts_min=2**4,
            n_counts_max=2**12,
            except_clipped_peak=False,
            # except_sloped_peak=False,
        ),
    )

    delta = 100
    for blink in blinks:
        left, right = blink.minima
        blink.minima = (max(left - delta, 0), min(right + delta, spectrum.n_numbers-1))

    if show:
        fig, ax = plt.subplots(figsize=(12, 4))

        plt.plot(
            datum.x,
            datum.y,
            color='black', linestyle='none', marker='.',
            label=r'$y$'
        )
        plt.plot(
            spectrum.index,
            spectrum.intensity,
            color='red', linestyle='-', linewidth=1,
            label=r'$\hat{y}$',
        )
        for blink in blinks:
            plt.axvline(
                np.mean(blink.maxima),
                color='red', linestyle=':',
            )

        plt.xlabel('Номер отсчета')
        plt.ylabel(r'$I$, %')
        plt.grid(color='grey', linestyle=':')
        plt.legend()

        plt.show()

    if len(blinks) < 2:
        raise ValueError('Not enough peaks found!')
    
    blinks = sorted(
        blinks,
        key=lambda blink: spectrum.intensity[blink.maxima[-1]],
        reverse=True,
    )[:2]

    blinks = sorted(
        blinks,
        key=lambda blink: blink.maxima[-1],
        reverse=False,
    )

    return blinks


def smooth_intensity(
    x: Array[N],
    y: Array[U],
    window: int,
) -> Array[U]:

    x = np.array(x)
    y = np.array(y)

    index = np.isnan(y) | np.isinf(y)
    if np.any(index):
        y[index] = np.interp(x[index], x[~index], y[~index])

    y_hat = signal.savgol_filter(y, window_length=window, polyorder=1)
    if np.any(index):
        y_hat[index] = THRESHOLD

    return y_hat
