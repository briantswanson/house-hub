from dataclasses import dataclass, field
from typing import Callable


@dataclass
class Scene:
    name: str
    description: str
    run: Callable
