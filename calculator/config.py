import dataclasses
import json
import os
from dataclasses import dataclass
from typing import Literal

from calculator.exceptions import ConfigLoadError
from calculator.types import GPa, MicroMeter, ReciprocalMeter, SampleName


# --------        detector        --------
PITCH = 12.5  # detector's width
THRESHOLD = 70  # detector's max output signal


# --------        report        --------
N_DIGITS = 2


# --------        experiment        --------
@dataclass(frozen=True, slots=True)
class Config:
    curvature_ref_standart: ReciprocalMeter
    curvature_flat_standart: ReciprocalMeter
    thickness_film: MicroMeter
    thickness_substrate: MicroMeter
    young_module: GPa
    stress_sign: Literal[-1, +1]

    def save(self, sample_name: SampleName) -> None:
        dat = dataclasses.asdict(self)

        filepath = os.path.join(os.getcwd(), 'data', sample_name, 'config.json')
        with open(filepath, 'w') as file:
            json.dump(dat, file)

    @classmethod
    def load(cls, sample_name: SampleName) -> 'Config':

        filepath = os.path.join(os.getcwd(), 'data', sample_name, 'config.json')
        try:
            with open(filepath, 'r') as file:
                dat = json.load(file)
        except FileNotFoundError:
            raise ConfigLoadError(f'Файл {filepath} не найден!')

        return cls(**dat)
