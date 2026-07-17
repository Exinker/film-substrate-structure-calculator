import os

from dotenv import load_dotenv

load_dotenv()


def _parse_version() -> str:
    default = '0.2'

    return os.environ.get('VERSION', None) or default


def _parse_detector_pitch() -> float:
    default = 12.5

    value = os.environ.get('DETECTOR_PITCH', None)
    if value is None:
        return default

    return float(value)


def _parse_threshold() -> float:
    default = 70

    value = os.environ.get('THRESHOLD', None)
    if value is None:
        return default

    return float(value)


def _parse_smooth_window() -> float:
    default = 20

    value = os.environ.get('SMOOTH_WINDOW', None)
    if value is None:
        return default

    return float(value)


VERSION = _parse_version()

DETECTOR_PITCH = _parse_detector_pitch()  # detector's width
THRESHOLD = _parse_threshold()  # detector's max output signal
SMOOTH_WINDOW = _parse_smooth_window()  # 


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
    DETECTOR_PITCH,
    THRESHOLD,
    VERSION,
]
