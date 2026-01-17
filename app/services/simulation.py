import asyncio
from dataclasses import dataclass

from app.runner.websocket import WebSocketManager
from app.services.locations import LocationsService
from app.services.movement import MovementService
from app.services.people import PeopleService


@dataclass
class SimulationService:
    websocket_manager: WebSocketManager
    people: PeopleService
    movement: MovementService
    locations: LocationsService

    async def broadcast_state(self) -> None:
        if self.websocket_manager.has_active_connections:
            people_data = [
                {
                    "id": person.id,
                    "location": {
                        "id": person.location.id,
                        "q": person.location.q,
                        "r": person.location.r,
                    },
                }
                for person in self.people.read_all()
            ]

            await self.websocket_manager.broadcast(people_data)

    async def run(self) -> None:
        while True:
            self.movement.move_all_people_randomly()
            await self.broadcast_state()
            await asyncio.sleep(1)
