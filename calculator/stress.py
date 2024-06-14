from dataclasses import dataclass
from typing import Mapping

from calculator.config import Config
from calculator.distance import Distance
from calculator.stats import Stats
from calculator.types import Array, Kind, FileDir, ReciprocalMeter


@dataclass(frozen=True, slots=True)
class Curvature:
    value: ReciprocalMeter | Array[ReciprocalMeter]
    filedir: FileDir

    @property
    def stats(self) -> Stats:
        return Stats.calculate(self.value)

    @classmethod
    def calculate(cls, distances: Mapping[Kind, Distance], config: Config) -> 'Curvature':
        k = config.curvature_ref_standart

        d = distances['sample'].value
        d_flat_standard = distances['flat-standard'].stats.value
        d_ref_standard = distances['ref-standard'].stats.value

        return cls(
            value=k * (d - d_flat_standard) / (d_ref_standard - d_flat_standard),
        )

    def __str__(self) -> str:
        return '[{}]'.format(
            '; '.join(map(str, self.value)),
        )
