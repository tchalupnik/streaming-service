import asyncio
import logging

import aio_pika
from aio_pika.abc import AbstractRobustConnection

from .base import MQBase
from .exceptions import MQError

logger = logging.getLogger(__name__)


class MQConnection(MQBase):
    async def connect(
        self, loop: asyncio.AbstractEventLoop = None
    ) -> AbstractRobustConnection:
        if loop is None:
            loop = asyncio.get_event_loop()
        try:
            connection = await aio_pika.connect_robust(
                self.settings.AMQP_URI, loop=loop
            )
            logger.info("AMQP created new connection")
        except ConnectionError:
            logger.error("AMQP cannot connect, connection refused!")
            raise MQError("Connection Error!")
        return connection
