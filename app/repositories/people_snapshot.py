import json
from dataclasses import asdict, dataclass
from pathlib import Path

from app.models.person import Location, Person


@dataclass
class SnapshotJsonRepository:
    snapshot_file: Path

    def __post_init__(self) -> None:
        self.snapshot_file.parent.mkdir(exist_ok=True)

    def save(self, people: list[Person]) -> None:
        raw = [asdict(p) for p in people]
        self.snapshot_file.write_text(json.dumps(raw, indent=2))

    def load(self) -> list[Person] | None:
        if not self.snapshot_file.exists():
            return None

        raw = json.loads(self.snapshot_file.read_text())

        return [
            Person(id=person["id"], location=Location(**person["location"]))
            for person in raw
        ]
