import dataclasses
import json
from dataclasses import dataclass
from typing import Literal

from calculator.exceptions import ConfigLoadError
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

    def save(self, name: str = 'config') -> None:
        dat = dataclasses.asdict(self)

        with open(f'{name}.json', 'w') as file:
            json.dump(dat, file)

    @classmethod
    def load(cls, name: str = 'config') -> 'Config':

        try:
            with open(f'{name}.json', 'r') as file:
                dat = json.load(file)
        except FileNotFoundError:
            raise ConfigLoadError('Файл `config.json` не найден!')

        return cls(**dat)
