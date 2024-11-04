from dataclasses import dataclass, field
from typing import ClassVar, NewType

import numpy as np
from scipy import stats

from calculator.types import Array


T = NewType('T', float)

N_DIGITS = 2


@dataclass(frozen=True, slots=True)
class Stats:
    value: T
    interval: T

    confidence_level: ClassVar[float] = field(default=0.95)

    @classmethod
    def calculate(cls, __value: Array[T]) -> 'Stats':
        n = len(__value)
        interval = stats.t.ppf((1 + cls.confidence_level)/2, n - 1) * np.std(__value, ddof=1) / np.sqrt(n)

        return cls(np.mean(__value), interval)

    def __str__(self) -> str:
        return fr'{np.round(self.value, N_DIGITS)} \pm {np.round(self.interval, N_DIGITS)}'
