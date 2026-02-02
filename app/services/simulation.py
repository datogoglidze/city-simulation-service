import asyncio
from dataclasses import asdict, dataclass

from app.services.actions import ActionsService
from app.services.movement import MovementService
from app.services.people import PeopleService
from app.services.websocket import WebSocketService


@dataclass
class SimulationService:
    websocket_manager: WebSocketService
    people: PeopleService
    movement: MovementService
    actions: ActionsService

    async def broadcast_state(self) -> None:
        if self.websocket_manager.has_active_connections:
            people = [asdict(person) for person in self.people.read_many()]
            await self.websocket_manager.broadcast(people)

    async def run(self) -> None:
        while True:
            self.actions.kill()
            self.movement.move_people_to_random_adjacent_location()
            await self.broadcast_state()
            await asyncio.sleep(1)
