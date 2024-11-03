VERSION = '0.2'

DETECTOR_PITCH = 12.5  # detector's width
DETECTOR_THRESHOLD = 70  # detector's max output signal

N_DIGITS = 2


match VERSION:
    case '0.1':
        from .config import (
            ConfigV01 as Config,
            DataKindV01 as DataKind,
        )
    case '0.2':
        from .config import (
            ConfigV02 as Config,
            DataKindV02 as DataKind,
        )


__all__ = [
    Config,
    DataKind,
    VERSION,
    DETECTOR_PITCH,
    DETECTOR_THRESHOLD,
    N_DIGITS,
]
