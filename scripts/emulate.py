import shutil

import pandas as pd

from spectrumlab.detectors import Detector

from calculator import ROOT
from tests.utils import emulate_spectrum


def run(
    n_iters: int = 10,
    sample_name: str = 'test',
) -> None:
    filedir = ROOT / 'data' / sample_name / sample_name
    if filedir.exists():
        shutil.rmtree(filedir)
    filedir.mkdir(parents=True)

    detector = Detector.BLPP369M1
    spectrum = emulate_spectrum(
        delta=0,
        width=100,
        amplitude=4,
        background=0,
        n_numbers=detector.config.shape[-1],
        n_frames=100,
    )

    for i in range(n_iters):
        pd.DataFrame({
            'wavelength': spectrum.wavelength,
            'intensity': spectrum.intensity,
            'crystal': 0,
            'clipped': 0,
        }).to_csv(
            filedir / '{sample_name} - {i}.txt'.format(
                sample_name=sample_name,
                i=i+1,
            ),
            sep='\t',
            index=False,
            header=False,
        )
