from dataclasses import dataclass


@dataclass
class Location:
    x: int
    y: int


@dataclass
class Person:
    id: int
    location: Location
