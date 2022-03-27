from pydantic import BaseModel


class BasePublisherMessage(BaseModel):
    pass


class BasePublisher:
    async def publish(self, message: BasePublisherMessage):
        raise NotImplementedError
