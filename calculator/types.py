from pathlib import Path
from typing import Literal, NewType, TypeAlias

from numpy.typing import NDArray

Kind = Literal['sample', 'ref-standard', 'flat-standard']
FileDir: TypeAlias = str | Path

Array: TypeAlias = NDArray
N = NewType('N', int)
U = NewType('U', float)

Inch = NewType('Inch', float)
Meter = NewType('Meter', float)
MicroMeter = NewType('MicroMeter', float)

ReciprocalMeter = NewType('ReciprocalMeter', float)

MPa = NewType('MPa', float)
GPa = NewType('GPa', float)
