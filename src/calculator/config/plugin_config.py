from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings


class PluginConfig(BaseSettings):

    version: Literal['0.1', '0.2'] = Field('0.2', alias='VERSION')
    detector_pitch: float = Field(12.5, ge=0, alias='DETECTOR_PITCH')
    threshold: float = Field(70, ge=0, le=100, alias='THRESHOLD')
    smooth_window: int = Field(20, ge=1, le=1000, alias='SMOOTH_WINDOW')


PLUGIN_CONFIG = PluginConfig()
