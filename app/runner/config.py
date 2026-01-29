import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    GRID_SIZE: int = int(os.getenv("GRID_SIZE", "100"))
    PEOPLE_AMOUNT: int = int(os.getenv("PEOPLE_AMOUNT", "100"))
    KILLER_PROBABILITY: float = float(os.getenv("KILLER_PROBABILITY", "0.1"))
    SNAPSHOT_PATH: str | None = os.getenv("SNAPSHOT_PATH")
    SNAPSHOT_INTERVAL: str | None = os.getenv("SNAPSHOT_INTERVAL")


config = Config()
