import logging

from streaming.exceptions import RegistryError
from streaming.mq.consumer import MQConsumer

logger = logging.getLogger(__name__)


class ConsumerRegistry:
    consumers = []

    @classmethod
    def register(cls, item):
        if isinstance(item, MQConsumer):
            cls.consumers.append(item)
        else:
            logger.error(f"Unrecognized type {type(item)}!")
            raise RegistryError("Unrecognized type!")
