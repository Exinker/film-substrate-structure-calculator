from dataclasses import dataclass

from calculator.config import Config
from calculator.length import LengthMap
from calculator.stats import Stats
from calculator.types import Array, ReciprocalMeter


@dataclass(frozen=True, slots=True)
class Curvature:
    value: ReciprocalMeter | Array[ReciprocalMeter]

    @property
    def stats(self) -> Stats:
        return Stats.calculate(self.value)

    @classmethod
    def calculate(cls, length: LengthMap, config: Config) -> 'Curvature':
        c_ref_standart = config.curvature_ref_standart

        d = length['sample'].value
        d_flat_standard = length['flat-standard'].stats.value
        d_ref_standard = length['ref-standard'].stats.value

        return cls(
            value=c_ref_standart * (d - d_flat_standard) / (d_ref_standard - d_flat_standard),
        )

    def __str__(self) -> str:
        return '[{}]'.format(
            '; '.join(map(str, self.value)),
        )
