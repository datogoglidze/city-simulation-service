import asyncio
from dataclasses import asdict, dataclass

from app.runner.websocket import WebSocketManager
from app.services.people import PeopleService


@dataclass
class SimulationService:
    websocket_manager: WebSocketManager
    people: PeopleService
    snapshot_interval: int

    async def broadcast_state(self) -> None:
        if self.websocket_manager.active_connections:
            people = [asdict(person) for person in self.people.get_all()]
            await self.websocket_manager.broadcast(people)

    async def run(self) -> None:
        iteration = 0
        while True:
            self.people.update_positions()
            await self.broadcast_state()

            iteration += 1
            if iteration == self.snapshot_interval:
                self.people.save_snapshot()
                iteration = 0

            await asyncio.sleep(1)
