import asyncio
import json
from dataclasses import asdict, dataclass

from app.core.people import PeopleService
from app.runner.websocket import WebSocketManager


@dataclass
class SimulationService:
    websocket_manager: WebSocketManager
    people_service: PeopleService

    async def broadcast_state(self) -> None:
        if self.websocket_manager.active_connections:
            people_data = [asdict(person) for person in self.people_service.get_all()]
            await self.websocket_manager.broadcast(json.dumps(people_data))

    async def run(self) -> None:
        while True:
            self.people_service.update_positions()
            await self.broadcast_state()
            await asyncio.sleep(1)
