import logging

import aio_pika
from aio_pika.abc import AbstractRobustChannel
from aiormq import ChannelInvalidStateError

from streaming.publisher import BasePublisher, BasePublisherMessage
from .base import MQBase
from .factories import MQChannelFactory
from .exceptions import MQError

logger = logging.getLogger(__name__)


class MQPublisher(MQBase, BasePublisher):
    routing_key: str
    channel: AbstractRobustChannel

    async def publish(self, message: BasePublisherMessage):
        if not hasattr(self, "channel"):
            self.channel = await MQChannelFactory.get_publisher_channel()

        exchange = await self.channel.get_exchange(self.settings.DEFAULT_EXCHANGE_NAME)
        logger.info(f"AMQP publishing message on: {self.routing_key}")
        try:
            await exchange.publish(
                aio_pika.Message(
                    body=message.json().encode(),
                    delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                ),
                routing_key=self.routing_key,
            )
        except ChannelInvalidStateError:
            raise MQError("AMQP Cannot publish message!")
