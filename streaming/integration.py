from streaming.mq.base import MQBase
from streaming.mq.consumer import MQConsumerExecutor
from streaming.mq.settings import MQSettings
from streaming.registry import ConsumerRegistry


class MQFastAPIEventSpawner(MQBase):
    def __init__(self, settings: MQSettings = None):
        super().__init__(settings)

    def spawn(self, app):
        for consumer in ConsumerRegistry.consumers:
            app.router.add_event_handler(
                "startup", MQConsumerExecutor(consumer, self.settings).execute
            )
