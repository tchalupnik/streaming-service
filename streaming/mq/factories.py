import aio_pika
from aio_pika.abc import (
    AbstractRobustConnection,
    AbstractRobustChannel,
    AbstractRobustExchange,
)

from streaming.mq.connection import logger, MQConnection
from streaming.mq.settings import MQSettings


class MQConnectionFactory:
    cached_connection: AbstractRobustConnection = None

    @staticmethod
    async def build(
        cls, settings: MQSettings = None, new: bool = False
    ) -> AbstractRobustConnection:
        if MQConnectionFactory.cached_connection and not new:
            logger.info("AMQP returned cached connection")
            return MQConnectionFactory.cached_connection

        connection = await MQConnection(settings).connect()
        MQConnectionFactory.cached_connection = connection
        return connection


class MQChannelFactory:
    cached_consumer_channel: AbstractRobustChannel = None
    cached_publisher_channel: AbstractRobustChannel = None

    @classmethod
    async def build(cls, settings: MQSettings = None) -> AbstractRobustChannel:
        connection = await MQConnectionFactory.build(settings)
        channel = await connection.channel()
        return channel

    @classmethod
    async def get_consumer_channel(cls) -> AbstractRobustChannel:
        if not MQChannelFactory.cached_consumer_channel:
            MQChannelFactory.cached_consumer_channel = await cls.build()

        return MQChannelFactory.cached_consumer_channel

    @classmethod
    async def get_publisher_channel(cls) -> AbstractRobustChannel:
        if not MQChannelFactory.cached_publisher_channel:
            MQChannelFactory.cached_publisher_channel = await cls.build()

        return MQChannelFactory.cached_publisher_channel


class MQExchangeFactory:
    cached_default_exchange: AbstractRobustExchange = None

    @classmethod
    async def build(cls, settings: MQSettings) -> AbstractRobustExchange:
        if MQExchangeFactory.cached_default_exchange:
            return MQExchangeFactory.cached_default_exchange

        channel = await MQChannelFactory.build(settings)
        exchange: AbstractRobustExchange = await channel.declare_exchange(
            settings.DEFAULT_EXCHANGE_NAME,
            type=aio_pika.ExchangeType.TOPIC,
            durable=True,
        )
        MQExchangeFactory.cached_default_exchange = exchange
        return exchange
