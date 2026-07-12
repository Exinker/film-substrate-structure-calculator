import os
from abc import ABC, abstractmethod

import numpy as np
import pandas as pd

from calculator.config import Config
from calculator.curvature import Curvature
from calculator.length import LengthMap
from calculator.stress import Stress
from calculator.types import SampleName


class ReportABC(ABC):

    def __init__(
        self,
        sample_name: SampleName,
        config: Config,
        length: LengthMap,
        curvature: Curvature,
        stress: Stress,
    ) -> None:
        self.sample_name = sample_name
        self.config = config
        self.length = length
        self.curvature = curvature
        self.stress = stress

    @abstractmethod
    def publish(self) -> None:
        raise NotImplementedError

    @classmethod
    def create(
        cls,
        sample_name: SampleName,
        config: Config,
        verbose: bool = False,
    ) -> None:
        length = LengthMap.calculate(
            sample_name=sample_name,
            verbose=verbose,
        )
        curvature = Curvature.calculate(
            length=length,
            config=config,
        )
        stress = Stress.calculate(
            curvature=curvature.value,
            config=config,
        )

        return cls(
            sample_name=sample_name,
            config=config,
            length=length,
            curvature=curvature,
            stress=stress,
        )


class ReportV01(ReportABC):

    def publish(self) -> None:

        # results sheet
        frame = pd.concat([
            pd.DataFrame({
                'index': ['Ср. знач.', 'Дов. инт.'],
                'l, мкм': [
                    self.length['sample'].stats.value,
                    self.length['sample'].stats.interval,
                ],
                'K, м-1': [
                    self.curvature.stats.value,
                    self.curvature.stats.interval,
                ],
                'σ, МПа': [
                    self.stress.stats.value,
                    self.stress.stats.interval,
                ],
            }).set_index('index', drop=True),
            pd.DataFrame({
                'index': [''],
                'l, мкм': [''],
                'K, м-1': [''],
                'σ, МПа': [''],
            }).set_index('index', drop=True),
            pd.DataFrame({
                'index': np.arange(1, len(self.length['sample'].value)+1),
                'l, мкм': self.length['sample'].value,
                'K, м-1': self.curvature.value,
                'σ, МПа': self.stress.value,
            }).set_index('index', drop=True),
        ])
        frame.index.name = ''
        frame.columns = pd.MultiIndex.from_product([[self.sample_name], frame.columns])

        write(
            frame,
            sample_name=self.sample_name,
            sheet_name=self.sample_name,
        )

        # flat-standard sheet
        frame = pd.concat([
            pd.DataFrame({
                'index': ['Ср. знач.', 'Дов. инт.'],
                'l_0, мкм': [
                    self.length['flat-standard'].stats.value,
                    self.length['flat-standard'].stats.interval,
                ],
            }).set_index('index', drop=True),
            pd.DataFrame({
                'index': [''],
                'l_0, мкм': [''],
            }).set_index('index', drop=True),
            pd.DataFrame({
                'index': np.arange(1, len(self.length['flat-standard'].value)+1),
                'l_0, мкм': self.length['flat-standard'].value,
            }).set_index('index', drop=True),
        ])
        frame.index.name = ''

        write(
            frame,
            sample_name=self.sample_name,
            sheet_name='I_0',
        )

        # ref-standard sheet
        frame = pd.concat([
            pd.DataFrame({
                'index': ['Ср. знач.', 'Дов. инт.'],
                'l_эт, мкм': [
                    self.length['ref-standard'].stats.value,
                    self.length['ref-standard'].stats.interval,
                ],
            }).set_index('index', drop=True),
            pd.DataFrame({
                'index': [''],
                'l_эт, мкм': [''],
            }).set_index('index', drop=True),
            pd.DataFrame({
                'index': np.arange(1, len(self.length['ref-standard'].value)+1),
                'l_эт, мкм': self.length['ref-standard'].value,
            }).set_index('index', drop=True),
        ])
        frame.index.name = ''

        write(
            frame,
            sample_name=self.sample_name,
            sheet_name='I_эт',
        )

        # config sheet
        frame = pd.DataFrame({
            'K_эт, м-1': [self.config.curvature_ref_standart],
            'K_0, м-1': [self.config.curvature_flat_standart],
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


class ReportV02(ReportABC):

    def publish(self) -> None:

        # results sheet
        frame = pd.concat([
            pd.DataFrame({
                'index': ['Ср. знач.', 'Дов. инт.'],
                'l, мкм': [
                    self.length['sample'].stats.value,
                    self.length['sample'].stats.interval,
                ],
                'K, м-1': [
                    self.curvature.stats.value,
                    self.curvature.stats.interval,
                ],
                'σ, МПа': [
                    self.stress.stats.value,
                    self.stress.stats.interval,
                ],
            }).set_index('index', drop=True),
            pd.DataFrame({
                'index': [''],
                'l, мкм': [''],
                'K, м-1': [''],
                'σ, МПа': [''],
            }).set_index('index', drop=True),
            pd.DataFrame({
                'index': np.arange(1, len(self.length['sample'].value)+1),
                'l, мкм': self.length['sample'].value,
                'K, м-1': self.curvature.value,
                'σ, МПа': self.stress.value,
            }).set_index('index', drop=True),
        ])
        frame.index.name = ''
        frame.columns = pd.MultiIndex.from_product([[self.sample_name], frame.columns])

        write(
            frame,
            sample_name=self.sample_name,
            sheet_name=self.sample_name,
        )

        # flat-standard sheet
        frame = pd.concat([
            pd.DataFrame({
                'index': ['Ср. знач.', 'Дов. инт.'],
                'l_0, мкм': [
                    self.length['flat-standard'].stats.value,
                    self.length['flat-standard'].stats.interval,
                ],
            }).set_index('index', drop=True),
            pd.DataFrame({
                'index': [''],
                'l_0, мкм': [''],
            }).set_index('index', drop=True),
            pd.DataFrame({
                'index': np.arange(1, len(self.length['flat-standard'].value)+1),
                'l_0, мкм': self.length['flat-standard'].value,
            }).set_index('index', drop=True),
        ])
        frame.index.name = ''

        write(
            frame,
            sample_name=self.sample_name,
            sheet_name='I_0',
        )

        # h sheet
        frame = pd.concat([
            pd.DataFrame({
                'index': ['Ср. знач.', 'Дов. инт.'],
                'h, мкм': [self.length['h'].stats.value, self.length['h'].stats.interval],
            }).set_index('index', drop=True),
            pd.DataFrame({
                'index': [''],
                'h, мкм': [''],
            }).set_index('index', drop=True),
            pd.DataFrame({
                'index': np.arange(1, len(self.length['h'].value)+1),
                'h, мкм': self.length['h'].value,
            }).set_index('index', drop=True),
        ])
        frame.index.name = ''

        write(
            frame,
            sample_name=self.sample_name,
            sheet_name='h',
        )

        # config sheet
        frame = pd.DataFrame({
            'H, мкм': [self.config.h],
            'K_0, м-1': [self.config.curvature_flat_standart],
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
