from dataclasses import dataclass

from calculator.config import Config
from calculator.stats import Stats
from calculator.types import Array, MPa, ReciprocalMeter


@dataclass(frozen=True, slots=True)
class Stress:
    value: MPa | Array[MPa]

    @property
    def stats(self) -> Stats:
        return Stats.calculate(self.value)

    @classmethod
    def calculate(cls, curvature: ReciprocalMeter | Array[ReciprocalMeter], config: Config) -> 'Stress':
        sign = config.stress_sign
        young_module = config.young_module
        c_flat_standart = config.curvature_flat_standart
        th_film = config.thickness_film
        th_substrate = config.thickness_substrate

        return cls(
            value=1e-3 * sign * (young_module * th_substrate**2) * (curvature - c_flat_standart) / (6 * th_film),
        )

    def __str__(self) -> str:
        return '[{}]'.format(
            '; '.join(map(str, self.value)),
        )
