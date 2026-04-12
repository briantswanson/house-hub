from dataclasses import dataclass
from typing import Callable


@dataclass
class Scene:
    name: str
    description: str
    run: Callable
