from datetime import datetime

from pydantic import BaseModel

from streaming.domain.spawner import StreamingSpawner
from streaming.mq.consumer import MQConsumer


class StreamingMessage(BaseModel):
    name: str
    time_until: datetime


class StreamingConsumer(MQConsumer):
    message_type = StreamingMessage
    routing_key = "streaming"
    queue_name = "streaming_service.streaming"

    async def consume(self, message: message_type):
        await StreamingSpawner().spawn(time_until=message.time_until, name=message.name)
