from dataclasses import dataclass


@dataclass(frozen=True)
class Location:
    q: int
    r: int
