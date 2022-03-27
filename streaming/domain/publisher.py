from datetime import datetime

from streaming.mq.publisher import MQPublisher
from streaming.publisher import BasePublisherMessage


class StreamingPublisherMessage(BasePublisherMessage):
    name: str
    time_until: datetime


class StreamingPublisher(MQPublisher):
    routing_key = "streaming"
    message_type = StreamingPublisherMessage
