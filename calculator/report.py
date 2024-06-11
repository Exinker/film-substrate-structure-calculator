import os
from dataclasses import dataclass

import numpy as np
import pandas as pd

from calculator.config import Config
from calculator.distance import Distance


@dataclass(frozen=True, slots=True)
class Report:
    distance: Distance
    config: Config

    def create(self) -> None:
        filedir = self.distance.filedir
        filepath = os.path.join(filedir, 'report.xlsx')

        # results sheet
        _, name = os.path.split(filedir)

        frame = pd.concat([
            pd.DataFrame({
                'index': ['Ср. знач.', 'Дов. инт.'],
                'l, мкм': [self.distance.stats.value, self.distance.stats.interval],
            }).set_index('index', drop=True),
            pd.DataFrame({
                'index': [''],
                'l, мкм': [''],
            }).set_index('index', drop=True),
            pd.DataFrame({
                'index': np.arange(1, len(self.distance.value)+1),
                'l, мкм': self.distance.value,
            }).set_index('index', drop=True),
        ])
        frame.index.name = ''
        frame.columns = pd.MultiIndex.from_product([[name], frame.columns])

        mode = 'a' if os.path.isfile(filepath) else 'w'
        if_sheet_exists = 'replace' if mode == 'a' else None
        with pd.ExcelWriter(filepath, mode=mode, if_sheet_exists=if_sheet_exists, engine='openpyxl') as writer:
            frame.to_excel(
                writer,
                sheet_name=name,
            )

        # calibration sheet

        # config sheet
        frame = pd.DataFrame({
            'R_эт, м': [self.config.radius_standart],
            'R_0, м': [self.config.radius_flat],
            'd_f, мкм': [self.config.thickness_film],
            'd_s, мкм': [self.config.thickness_substrate],
            'E_s/(1 - nu_s), ГПа': [self.config.young_module],
            'Знак σ': [self.config.stress_sign],
        })

        mode = 'a' if os.path.isfile(filepath) else 'w'
        if_sheet_exists = 'replace' if mode == 'a' else None
        with pd.ExcelWriter(filepath, mode=mode, if_sheet_exists=if_sheet_exists, engine='openpyxl') as writer:
            frame.to_excel(
                writer,
                sheet_name='config',
                index=None,
            )
