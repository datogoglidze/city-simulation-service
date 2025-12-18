import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    GRID_SIZE: int = int(os.getenv("GRID_SIZE", "100"))
    PEOPLE_AMOUNT: int = int(os.getenv("PEOPLE_AMOUNT", "100"))
    SNAPSHOT_INTERVAL: int = int(os.getenv("SNAPSHOT_INTERVAL", "50"))
    SNAPSHOT_PATH: str = os.getenv("SNAPSHOT_PATH", "data/people_snapshot.json")


config = Config()
