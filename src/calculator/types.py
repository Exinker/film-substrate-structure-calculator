from typing import NewType, TypeAlias

from numpy.typing import NDArray
import pandas as pd


SampleName = NewType('SampleName', str)

Array: TypeAlias = NDArray
Frame: TypeAlias = pd.DataFrame

N = NewType('N', int)
U = NewType('U', float)

Inch = NewType('Inch', float)
Meter = NewType('Meter', float)
MicroMeter = NewType('MicroMeter', float)

ReciprocalMeter = NewType('ReciprocalMeter', float)

MPa = NewType('MPa', float)
GPa = NewType('GPa', float)
