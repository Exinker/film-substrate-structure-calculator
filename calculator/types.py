from typing import NewType, TypeAlias

from numpy.typing import NDArray


Array: TypeAlias = NDArray

N = NewType('N', int)
U = NewType('U', float)

Inch = NewType('Inch', float)
Meter = NewType('Meter', float)
MicroMeter = NewType('MicroMeter', float)
