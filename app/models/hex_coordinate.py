from abc import ABC, abstractmethod
from dataclasses import dataclass

from app.models.person import Location


class HexCoordinateStrategy(ABC):
    @abstractmethod
    def axial_to_offset(self, q: int, r: int) -> tuple[int, int]:
        pass

    @abstractmethod
    def offset_to_axial(self, col: int, row: int) -> tuple[int, int]:
        pass

    def is_within_grid_bounds(self, q: int, r: int, grid_size: int) -> bool:
        col, row = self.axial_to_offset(q, r)
        return 0 <= col < grid_size and 0 <= row < grid_size

    def generate_valid_locations(self, grid_size: int) -> list[Location]:
        valid_positions = []
        for row in range(grid_size):
            for col in range(grid_size):
                q, r = self.offset_to_axial(col, row)
                valid_positions.append(Location(q=q, r=r))
        return valid_positions


class OddRStrategy(HexCoordinateStrategy):
    def axial_to_offset(self, q: int, r: int) -> tuple[int, int]:
        col = q + (r - (r & 1)) // 2
        row = r
        return col, row

    def offset_to_axial(self, col: int, row: int) -> tuple[int, int]:
        q = col - (row - (row & 1)) // 2
        r = row
        return q, r


class EvenRStrategy(HexCoordinateStrategy):
    def axial_to_offset(self, q: int, r: int) -> tuple[int, int]:
        col = q + (r + (r & 1)) // 2
        row = r
        return col, row

    def offset_to_axial(self, col: int, row: int) -> tuple[int, int]:
        q = col - (row + (row & 1)) // 2
        r = row
        return q, r


class AxialStrategy(HexCoordinateStrategy):
    def axial_to_offset(self, q: int, r: int) -> tuple[int, int]:
        return q, r

    def offset_to_axial(self, col: int, row: int) -> tuple[int, int]:
        return col, row


@dataclass
class HexCoordinateSystem:
    strategy: HexCoordinateStrategy

    def axial_to_offset(self, location: Location) -> tuple[int, int]:
        return self.strategy.axial_to_offset(location.q, location.r)

    def offset_to_axial(self, col: int, row: int) -> Location:
        q, r = self.strategy.offset_to_axial(col, row)
        return Location(q=q, r=r)

    def is_within_bounds(self, location: Location, grid_size: int) -> bool:
        return self.strategy.is_within_grid_bounds(location.q, location.r, grid_size)

    def generate_valid_locations(self, grid_size: int) -> list[Location]:
        return self.strategy.generate_valid_locations(grid_size)
