import asyncio
import json
import random
from dataclasses import asdict, dataclass

from fastapi import APIRouter, WebSocket
from fastapi.websockets import WebSocketDisconnect

from app.runner.websocket import ConnectionManager

router = APIRouter(prefix="/simulation", tags=["Simulation"])


@dataclass
class Person:
    id: int
    x: int
    y: int


people = [
    Person(id=i, x=random.randint(0, 99), y=random.randint(0, 99)) for i in range(10)
]


async def run_simulation(manager: ConnectionManager) -> None:
    while True:
        for person in people:
            person.x = (person.x + random.choice([-1, 0, 1])) % 100
            person.y = (person.y + random.choice([-1, 0, 1])) % 100

        if manager.active_connections:
            await manager.broadcast(json.dumps([asdict(person) for person in people]))

        await asyncio.sleep(1)


@router.get("/people")
def get_people() -> list[Person]:
    return people


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    manager: ConnectionManager = websocket.app.state.manager
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
