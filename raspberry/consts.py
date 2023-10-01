from enum import StrEnum

from core import mixins as core_mixins


class TaskAction(core_mixins.EnumExtraMethodsMixin, StrEnum):
    ON = "on"
    OFF = "off"


class Task(core_mixins.EnumExtraMethodsMixin, StrEnum):
    LED = "LEDSocketTask"
    BUZZER = "BuzzerTask"


class SensorMeasurementUnit(core_mixins.EnumExtraMethodsMixin, StrEnum):
    temperature = "°C"
    humidity = "Rh"
    sound = "dB"
    light = "nm"
