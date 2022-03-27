from pydantic import BaseModel


class BaseConsumerMessage(BaseModel):
    pass


class BaseConsumer:
    message_type: BaseConsumerMessage = None

    async def consume(self, message: message_type):
        raise NotImplementedError
