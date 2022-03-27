import asyncio
import logging
from typing import Dict, List

from starlette.websockets import WebSocket

logger = logging.getLogger(__name__)


class WSConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, id: str):
        logger.info(f"WebSockets: Connect {id}")
        await websocket.accept()
        if id not in self.active_connections:
            self.active_connections[id] = []
        self.active_connections[id].append(websocket)

    def disconnect(self, id: str, websocket: WebSocket):
        logger.info(f"WebSockets: Disconnect {id}")
        if id in self.active_connections:
            self.active_connections[id] = [
                ac for ac in self.active_connections[id] if ac != websocket
            ]

    async def send_personal_message(self, message: str, id: str):
        logger.info(f"WebSockets: Publishing for {id}")
        if id in self.active_connections:
            await asyncio.gather(
                *[
                    connection.send_text(message)
                    for connection in self.active_connections[id]
                ]
            )

    async def broadcast(self, message: str):
        await asyncio.gather(
            *[
                connection.send_text(message)
                for connections in self.active_connections.values()
                for connection in connections
            ]
        )


class WSConnectionManagerFactory:
    manager: WSConnectionManager = None

    @classmethod
    def create(cls, cached=True):
        if not WSConnectionManagerFactory.manager or not cached:
            manager = WSConnectionManager()
            if cached:
                WSConnectionManagerFactory.manager = manager
        else:
            manager = WSConnectionManagerFactory.manager

        return manager
