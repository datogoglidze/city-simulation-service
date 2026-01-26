import asyncio
from dataclasses import asdict, dataclass

from app.runner.websocket import WebSocketManager
from app.services.movement import MovementService
from app.services.people import PeopleService


@dataclass
class SimulationService:
    websocket_manager: WebSocketManager
    people: PeopleService
    movement: MovementService

    async def broadcast_state(self) -> None:
        if self.websocket_manager.has_active_connections:
            people = [asdict(person) for person in self.people.read_all()]
            await self.websocket_manager.broadcast(people)

    async def run(self) -> None:
        while True:
            self.movement.move_people_to_random_adjacent_location()
            await self.broadcast_state()
            await asyncio.sleep(1)
