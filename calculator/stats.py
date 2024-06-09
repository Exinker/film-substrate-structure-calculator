import numpy as np
from dataclasses import dataclass, field
from scipy import stats
from typing import ClassVar, NewType

from calculator.types import Array

T = NewType('T', int)


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
        return fr'{self.value:.2f} \pm {self.interval:.2f}'
