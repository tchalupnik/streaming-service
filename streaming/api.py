import logging
from datetime import datetime, timedelta

from fastapi import Depends
from fastapi_utils.inferring_router import InferringRouter
from pydantic import PositiveInt
from starlette import status
from starlette.websockets import WebSocket, WebSocketDisconnect

from streaming.domain.spawner import StreamingSpawner
from streaming.ws import WSConnectionManager, WSConnectionManagerFactory

router = InferringRouter()

logger = logging.getLogger(__name__)


async def ws_manager_dep():
    manager = WSConnectionManagerFactory.create()
    yield manager


@router.websocket("/ws/{name}")
async def process(
    websocket: WebSocket,
    name: str,
    ws_manager: WSConnectionManager = Depends(ws_manager_dep),
):
    await ws_manager.connect(websocket, name)
    try:
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        ws_manager.disconnect(name, websocket)


@router.post("/notify", status_code=status.HTTP_201_CREATED)
async def notify(
    name: str,
    time_until_minutes: PositiveInt,
):
    await StreamingSpawner().spawn(
        time_until=datetime.utcnow() + timedelta(minutes=time_until_minutes), name=name
    )
