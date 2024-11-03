from calculator.config import VERSION


match VERSION:
    case '0.1':
        from .report import ReportV01 as Report
    case '0.2':
        from .report import ReportV02 as Report


__all__ = [
    Report,
]
