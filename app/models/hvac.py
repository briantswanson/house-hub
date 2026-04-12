from dataclasses import dataclass


@dataclass
class HVACUnit:
    id: str
    name: str
    room: str
    on: bool
    mode: str        # cool, heat, fan, auto, dry
    temperature: int  # fahrenheit
    fan_speed: str   # low, medium, high, auto
