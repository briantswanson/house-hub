from dataclasses import dataclass
from typing import Optional


@dataclass
class Light:
    id: str
    name: str
    room: str
    on: bool
    brightness: int          # 0-100
    color_temp: Optional[int] = None   # kelvin
