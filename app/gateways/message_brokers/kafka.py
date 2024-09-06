from dataclasses import dataclass
import orjson
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

from domain.interfaces.message_broker import BaseMessageBroker


@dataclass
class KafkaMessageBroker(BaseMessageBroker):
    producer: AIOKafkaProducer
    consumer: AIOKafkaConsumer

    async def start(self):
        await self.producer.start()
        await self.consumer.start()

    async def close(self):
        await self.producer.stop()
        await self.consumer.stop()

    async def send_message(self, key: str, value: bytes):
        await self.producer.send(topic=key, value=value)

    async def start_consuming(self, topic: str):
        await self.consumer.subscribe(topics=[topic])

        async for message in self.consumer:
            yield orjson.loads(message.value)

    async def stop_consuming(self):
        await self.consumer.unsubscribe()
