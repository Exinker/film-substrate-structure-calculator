import os
from abc import ABC, abstractmethod
from dataclasses import dataclass

import numpy as np
import pandas as pd

from calculator.config import Config
from calculator.curvature import Curvature
from calculator.length import LengthMap
from calculator.stress import Stress
from calculator.types import SampleName


class ReportABC(ABC):

    @abstractmethod
    def create(self, verbose: bool = False) -> None:
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class ReportV01(ReportABC):
    sample_name: SampleName
    config: Config

    def create(self, verbose: bool = False) -> None:

        length = LengthMap.calculate(
            sample_name=self.sample_name,
            verbose=verbose,
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
        frame.columns = pd.MultiIndex.from_product([[self.sample_name], frame.columns])

        write(
            frame,
            sample_name=self.sample_name,
            sheet_name=self.sample_name,
        )

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

        write(
            frame,
            sample_name=self.sample_name,
            sheet_name='ref-standard',
        )

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

        write(
            frame,
            sample_name=self.sample_name,
            sheet_name='flat-standard',
        )

        # config sheet
        frame = pd.DataFrame({
            'K_эт, м': [self.config.curvature_ref_standart],
            'K_0, м': [self.config.curvature_flat_standart],
            'd_f, мкм': [self.config.thickness_film],
            'd_s, мкм': [self.config.thickness_substrate],
            'E_s/(1 - nu_s), ГПа': [self.config.young_module],
            'Знак σ': [self.config.stress_sign],
        })
        frame.index = ['']

        write(
            frame,
            sample_name=self.sample_name,
            sheet_name='config',
        )


@dataclass(frozen=True, slots=True)
class ReportV02(ReportABC):
    sample_name: SampleName
    config: Config

    def create(self, verbose: bool = False) -> None:

        length = LengthMap.calculate(
            sample_name=self.sample_name,
            verbose=verbose,
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
        frame.columns = pd.MultiIndex.from_product([[self.sample_name], frame.columns])

        write(
            frame,
            sample_name=self.sample_name,
            sheet_name=self.sample_name,
        )

        # h sheet
        frame = pd.concat([
            pd.DataFrame({
                'index': ['Ср. знач.', 'Дов. инт.'],
                'h, мкм': [length['h'].stats.value, length['h'].stats.interval],
            }).set_index('index', drop=True),
            pd.DataFrame({
                'index': [''],
                'h, мкм': [''],
            }).set_index('index', drop=True),
            pd.DataFrame({
                'index': np.arange(1, len(length['h'].value)+1),
                'h, мкм': length['h'].value,
            }).set_index('index', drop=True),
        ])
        frame.index.name = ''

        write(
            frame,
            sample_name=self.sample_name,
            sheet_name='h',
        )

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

        write(
            frame,
            sample_name=self.sample_name,
            sheet_name='I0',
        )

        # config sheet
        frame = pd.DataFrame({
            'H, мкм': [self.config.h],
            'K_0, м': [self.config.curvature_flat_standart],
            'd_f, мкм': [self.config.thickness_film],
            'd_s, мкм': [self.config.thickness_substrate],
            'E_s/(1 - nu_s), ГПа': [self.config.young_module],
            'Знак σ': [self.config.stress_sign],
        })
        frame.index = ['']

        write(
            frame,
            sample_name=self.sample_name,
            sheet_name='config',
        )


def write(frame: pd.DataFrame, sample_name: SampleName, sheet_name: str) -> None:
    """Write frame to selected sheet."""
    filedir = os.path.join(os.getcwd(), 'data', sample_name)
    filepath = os.path.join(filedir, 'report.xlsx')

    mode = 'a' if os.path.isfile(filepath) else 'w'
    if_sheet_exists = 'replace' if mode == 'a' else None
    with pd.ExcelWriter(filepath, mode=mode, if_sheet_exists=if_sheet_exists, engine='openpyxl') as writer:
        frame.to_excel(
            writer,
            sheet_name=sheet_name,
        )
