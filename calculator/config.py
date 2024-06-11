import dataclasses
import json
from dataclasses import dataclass
from typing import Literal

from calculator.types import GPa, Meter, MicroMeter


# --------        detector        --------
PITCH = 12.5  # detector's width
THRESHOLD = 70  # detector's max output signal


# --------        report        --------
N_DIGITS = 2


# --------        experiment        --------
@dataclass(frozen=True, slots=True)
class Config:
    radius_standart: Meter
    radius_flat: Meter
    thickness_film: MicroMeter
    thickness_substrate: MicroMeter
    young_module: GPa
    stress_sign: Literal[-1, +1]

    def save(self, name: str) -> None:
        dat = dataclasses.asdict(self)

        with open(f'{name}.json', 'w') as file:
            json.dump(dat, file)

    @classmethod
    def default(cls) -> 'Config':
        return cls(
            radius_standart=20.3,
            radius_flat=-197,
            thickness_film=0.191,
            thickness_substrate=390,
            young_module=180.5,
            stress_sign=-1,
        )

    @classmethod
    def load(cls, name: str = 'config') -> 'Config':

        with open(f'{name}.json', 'r') as file:
            dat = json.load(file)

        return cls(**dat)
