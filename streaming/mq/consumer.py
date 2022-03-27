import json
import logging

from aio_pika.abc import AbstractIncomingMessage

from streaming.consumer import BaseConsumer
from .base import MQBase
from .factories import MQChannelFactory, MQExchangeFactory
from .settings import MQSettings

logger = logging.getLogger(__name__)


class MQConsumer(BaseConsumer):
    queue_name: str = None
    routing_key: str = None


class ConsumerProcessor:
    def __init__(self, consumer: MQConsumer):
        self.consumer = consumer

    async def process(self, message: AbstractIncomingMessage):
        async with message.process():
            logger.info(f"AMQP processing message from {message.routing_key}")
            serialized_data = json.loads(message.body.decode())
            serialized_message = self.consumer.message_type.parse_obj(serialized_data)
            await self.consumer.consume(serialized_message)


class MQConsumerExecutor(MQBase):
    def __init__(self, consumer: MQConsumer, settings: MQSettings = None):
        super().__init__(settings)
        self.consumer = consumer

    async def execute(self):
        channel = await MQChannelFactory.get_consumer_channel()
        queue = await channel.declare_queue(self.consumer.queue_name)
        exchange = await MQExchangeFactory.build(self.settings)
        await queue.bind(exchange, routing_key=self.consumer.routing_key)
        processor = ConsumerProcessor(self.consumer)
        await queue.consume(processor.process)
