import asyncio
from dataclasses import asdict, dataclass

from app.repositories.people_snapshot import SnapshotJsonRepository
from app.runner.websocket import WebSocketManager
from app.services.people import PeopleService


@dataclass
class SimulationService:
    websocket_manager: WebSocketManager
    snapshot: SnapshotJsonRepository
    people: PeopleService
    snapshot_interval: int

    def _get_current_state(self) -> list[dict]:
        """Get the current simulation state."""
        return [asdict(person) for person in self.people.read_all()]

    async def send_state_to(self, websocket) -> None:
        """Send current state to a specific client."""
        state = self._get_current_state()
        await self.websocket_manager.send(websocket, state)

    async def broadcast_state(self) -> None:
        """Broadcast current state to all connected clients."""
        if self.websocket_manager.has_active_connections:
            state = self._get_current_state()
            await self.websocket_manager.broadcast(state)

    async def run(self) -> None:
        iteration = 0
        while True:
            self.people.update_location()
            await self.broadcast_state()

            iteration += 1
            if iteration == self.snapshot_interval:
                self.snapshot.save(self.people.read_all())
                iteration = 0

            await asyncio.sleep(1)
