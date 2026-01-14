import os

from dotenv import load_dotenv

from app.services.hex_coordinate_strategies import (
    AxialStrategy,
    EvenRStrategy,
    HexCoordinateStrategy,
    OddRStrategy,
)

load_dotenv()


class Config:
    GRID_SIZE: int = int(os.getenv("GRID_SIZE", "100"))
    PEOPLE_AMOUNT: int = int(os.getenv("PEOPLE_AMOUNT", "100"))
    SNAPSHOT_INTERVAL: int = int(os.getenv("SNAPSHOT_INTERVAL", "50"))
    SNAPSHOT_PATH: str = os.getenv("SNAPSHOT_PATH", "data/people_snapshot.json")
    HEX_COORDINATE_SYSTEM: str = os.getenv("HEX_COORDINATE_SYSTEM", "odd-r")

    @staticmethod
    def get_coordinate_strategy() -> HexCoordinateStrategy:
        system = Config.HEX_COORDINATE_SYSTEM.lower()

        if system == "odd-r":
            return OddRStrategy()
        elif system == "even-r":
            return EvenRStrategy()
        elif system == "axial":
            return AxialStrategy()
        else:
            raise ValueError(
                f"Unknown hex coordinate system: {system}. "
                "Use 'odd-r', 'even-r', or 'axial'"
            )


config = Config()
