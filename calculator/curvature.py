from dataclasses import dataclass

from calculator.config import Config, VERSION
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

        if VERSION == '0.1':
            c_ref_standart = config.curvature_ref_standart

            l_sample = length['sample'].value
            l_flat_standard = length['flat-standard'].stats.value
            l_ref_standard = length['ref-standard'].stats.value

            return cls(
                value=c_ref_standart * (l_sample - l_flat_standard) / (l_ref_standard - l_flat_standard),
            )

        if VERSION == '0.2':
            h = config.h

            l_sample = length['sample'].value
            l_flat_standard = length['flat-standard'].stats.value
            l_h = length['h'].stats.value

            return cls(
                value=(l_sample - l_flat_standard) / (2*h*l_h/10**6),
            )

        raise ValueError(f'Version {VERSION} is not supported yet!')

    def __str__(self) -> str:
        return '[{}]'.format(
            '; '.join(map(str, self.value)),
        )
