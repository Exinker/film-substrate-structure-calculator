import os
from dataclasses import dataclass

import numpy as np
import pandas as pd

from calculator.config import Config
from calculator.curvature import Curvature
from calculator.length import LengthMap
from calculator.stress import Stress


@dataclass(frozen=True, slots=True)
class Report:
    name: str
    config: Config

    def create(self) -> None:

        length = LengthMap.calculate(
            name=self.name,
        )
        curvature = Curvature.calculate(
            length=length,
            config=self.config,
        )
        stress = Stress.calculate(
            curvature=curvature.value,
            config=self.config,
        )

        # results sheet
        frame = pd.concat([
            pd.DataFrame({
                'index': ['Ср. знач.', 'Дов. инт.'],
                'l, мкм': [length['sample'].stats.value, length['sample'].stats.interval],
                'K, м-1': [curvature.stats.value, curvature.stats.interval],
                'σ, МПа': [stress.stats.value, stress.stats.interval],
            }).set_index('index', drop=True),
            pd.DataFrame({
                'index': [''],
                'l, мкм': [''],
                'K, м-1': [''],
                'σ, МПа': [''],
            }).set_index('index', drop=True),
            pd.DataFrame({
                'index': np.arange(1, len(length['sample'].value)+1),
                'l, мкм': length['sample'].value,
                'K, м-1': curvature.value,
                'σ, МПа': stress.value,
            }).set_index('index', drop=True),
        ])
        frame.index.name = ''
        frame.columns = pd.MultiIndex.from_product([[self.name], frame.columns])

        write(frame, name=self.name, sheet_name=self.name)

        # ref-standard sheet
        frame = pd.concat([
            pd.DataFrame({
                'index': ['Ср. знач.', 'Дов. инт.'],
                'l_эт, мкм': [length['ref-standard'].stats.value, length['ref-standard'].stats.interval],
            }).set_index('index', drop=True),
            pd.DataFrame({
                'index': [''],
                'l_эт, мкм': [''],
            }).set_index('index', drop=True),
            pd.DataFrame({
                'index': np.arange(1, len(length['ref-standard'].value)+1),
                'l_эт, мкм': length['ref-standard'].value,
            }).set_index('index', drop=True),
        ])
        frame.index.name = ''

        write(frame, name=self.name, sheet_name='ref-standard')

        # flat-standard sheet
        frame = pd.concat([
            pd.DataFrame({
                'index': ['Ср. знач.', 'Дов. инт.'],
                'l_0, мкм': [length['flat-standard'].stats.value, length['flat-standard'].stats.interval],
            }).set_index('index', drop=True),
            pd.DataFrame({
                'index': [''],
                'l_0, мкм': [''],
            }).set_index('index', drop=True),
            pd.DataFrame({
                'index': np.arange(1, len(length['flat-standard'].value)+1),
                'l_0, мкм': length['flat-standard'].value,
            }).set_index('index', drop=True),
        ])
        frame.index.name = ''

        write(frame, name=self.name, sheet_name='flat-standard')

        # config sheet
        frame = pd.DataFrame({
            'R_эт, м': [self.config.curvature_ref_standart],
            'R_0, м': [self.config.curvature_flat_standart],
            'd_f, мкм': [self.config.thickness_film],
            'd_s, мкм': [self.config.thickness_substrate],
            'E_s/(1 - nu_s), ГПа': [self.config.young_module],
            'Знак σ': [self.config.stress_sign],
        })
        frame.index = ['']

        write(frame, name=self.name, sheet_name='config')


def write(frame: pd.DataFrame, name: str, sheet_name: str) -> None:
    """Write frame to selected sheet."""
    filedir = os.path.join(os.getcwd(), 'data', name)
    filepath = os.path.join(filedir, 'report.xlsx')

    mode = 'a' if os.path.isfile(filepath) else 'w'
    if_sheet_exists = 'replace' if mode == 'a' else None
    with pd.ExcelWriter(filepath, mode=mode, if_sheet_exists=if_sheet_exists, engine='openpyxl') as writer:
        frame.to_excel(
            writer,
            sheet_name=sheet_name,
        )
