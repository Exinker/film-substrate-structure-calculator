from .plugin_config import PLUGIN_CONFIG

match PLUGIN_CONFIG.version:
    case '0.1':
        from .data_config import (
            DataConfigV01 as Config,
            DataKindV01 as DataKind,
        )
    case '0.2':
        from .data_config import (
            DataConfigV02 as Config,
            DataKindV02 as DataKind,
        )


__all__ = [
    Config,
    DataKind,
    PLUGIN_CONFIG,
]
