import dataclasses
import json
import os
from dataclasses import dataclass
from typing import Literal

from calculator.exceptions import ConfigLoadError
from calculator.types import GPa, MicroMeter, ReciprocalMeter, SampleName

DataKindV01 = Literal['sample', 'flat-standard', 'ref-standard']
DataKindV02 = Literal['sample', 'flat-standard', 'h']


class ConfigABC:

    def save(self, sample_name: SampleName) -> None:
        dat = dataclasses.asdict(self)

        filepath = os.path.join(os.getcwd(), 'data', sample_name, 'config.json')
        with open(filepath, 'w') as file:
            json.dump(dat, file)

    @classmethod
    def load(cls, sample_name: SampleName) -> 'ConfigABC':

        filepath = os.path.join(os.getcwd(), 'data', sample_name, 'config.json')
        try:
            with open(filepath, 'r') as file:
                dat = json.load(file)
        except FileNotFoundError:
            raise ConfigLoadError(f'Файл {filepath} не найден!')

        return cls(**dat)


@dataclass(frozen=True, slots=True)
class ConfigV01(ConfigABC):
    curvature_ref_standart: ReciprocalMeter
    curvature_flat_standart: ReciprocalMeter
    thickness_film: MicroMeter
    thickness_substrate: MicroMeter
    young_module: GPa
    stress_sign: Literal[-1, +1]


@dataclass(frozen=True, slots=True)
class ConfigV02(ConfigABC):
    h: MicroMeter
    curvature_flat_standart: ReciprocalMeter
    thickness_film: MicroMeter
    thickness_substrate: MicroMeter
    young_module: GPa
    stress_sign: Literal[-1, +1]
