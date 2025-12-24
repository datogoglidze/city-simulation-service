from dataclasses import dataclass


@dataclass
class ExistsError(Exception):
    id: str


@dataclass
class DoesNotExistError(Exception):
    id: str
