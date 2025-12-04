import json

import aio_pika

from app.config import Settings


async def publish_delivery_event(data: dict):
    connection = await aio_pika.connect_robust(
        f"amqp://guest:guest@{Settings.RABBITMQ_HOST}:{Settings.RABBITMQ_PORT}"
    )

    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue(Settings.RABBITMQ_QUEUE, auto_delete=True)

        message = aio_pika.Message(
            body=json.dumps(data).encode(),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
        )

        await channel.default_exchange.publish(
            message,
            routing_key=Settings.RABBITMQ_QUEUE,
        )
