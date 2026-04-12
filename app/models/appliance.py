from dataclasses import dataclass


@dataclass
class Appliance:
    id: str
    name: str
    type: str    # washer, dryer, dishwasher, range, microwave, tv, water_heater
    state: str   # on, off, running, paused, finished
