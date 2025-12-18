import asyncio
from dataclasses import asdict, dataclass

from app.core.people import PeopleService
from app.runner.websocket import WebSocketManager


@dataclass
class SimulationService:
    websocket_manager: WebSocketManager
    people: PeopleService

    async def broadcast_state(self) -> None:
        if self.websocket_manager.active_connections:
            people = [asdict(person) for person in self.people.get_all()]
            await self.websocket_manager.broadcast(people)

    async def run(self) -> None:
        while True:
            self.people.update_positions()
            await self.broadcast_state()
            await asyncio.sleep(1)
