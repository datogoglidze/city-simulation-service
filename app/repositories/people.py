import json
from dataclasses import dataclass
from pathlib import Path

from app.models.person import Person


@dataclass
class PeopleJsonRepository:
    snapshot_file: Path

    def __post_init__(self) -> None:
        self.snapshot_file.parent.mkdir(exist_ok=True)

    def save_snapshot(self, people: list[Person]) -> None:
        raw = [{"id": p.id, "x": p.x, "y": p.y} for p in people]
        self.snapshot_file.write_text(json.dumps(raw, indent=2))

    def load_snapshot(self) -> list[Person] | None:
        if not self.snapshot_file.exists():
            return None

        raw = json.loads(self.snapshot_file.read_text())
        return [Person(**person) for person in raw]
