import logging

from fastapi import FastAPI

from streaming.api import router
from streaming.domain.consumer import StreamingConsumer
from streaming.integration import MQFastAPIEventSpawner
from streaming.registry import ConsumerRegistry

logger = logging.getLogger(__name__)
logging.basicConfig(level="INFO", format="[%(asctime)s] %(levelname)s - %(message)s")


def get_app():
    ConsumerRegistry.register(StreamingConsumer())
    app = FastAPI()
    app.include_router(router)
    MQFastAPIEventSpawner().spawn(app)
    return app


app = get_app()
