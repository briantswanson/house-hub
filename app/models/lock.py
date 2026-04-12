from dataclasses import dataclass


@dataclass
class Lock:
    id: str
    name: str
    locked: bool
