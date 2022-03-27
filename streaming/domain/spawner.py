import asyncio
import logging
from datetime import datetime
from random import random

from streaming.domain.publisher import StreamingPublisher, StreamingPublisherMessage
from streaming.ws import WSConnectionManagerFactory, WSConnectionManager

DELAY_IN_SECONDS = 5

logger = logging.getLogger(__name__)


class StreamingSpawner:
    def __init__(self):
        self.ws_manager: WSConnectionManager = WSConnectionManagerFactory.create()
        self.publisher = StreamingPublisher()

    async def spawn(self, time_until: datetime, name: str):
        logger.info(f"Spawning with attributes: name {name}, time_until {time_until}")
        if time_until >= datetime.utcnow():
            await self.ws_manager.send_personal_message(str(random()), name)
            asyncio.create_task(asyncio.sleep(DELAY_IN_SECONDS)).add_done_callback(
                lambda _: asyncio.create_task(
                    self.publisher.publish(
                        message=StreamingPublisherMessage(
                            name=name,
                            time_until=time_until,
                        )
                    )
                )
            )

        else:
            logger.info(f"Spawner has finished spawning for name: {name}")
