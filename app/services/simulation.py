import asyncio
from dataclasses import asdict, dataclass

from app.runner.websocket import WebSocketManager
from app.services.people import PeopleService
from app.services.snapshot import SnapshotService


@dataclass
class SimulationService:
    websocket_manager: WebSocketManager
    snapshot: SnapshotService
    people: PeopleService
    snapshot_interval: int

    async def broadcast_state(self) -> None:
        if self.websocket_manager.has_active_connections:
            people = [asdict(person) for person in self.people.get_all()]
            await self.websocket_manager.broadcast(people)

    async def run(self) -> None:
        iteration = 0
        while True:
            self.people.update_positions()
            await self.broadcast_state()

            iteration += 1
            if iteration == self.snapshot_interval:
                self.snapshot.save(self.people.get_all())
                iteration = 0

            await asyncio.sleep(1)
