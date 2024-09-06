from core.ioc import init_container
from core.config import settings
from domain.logic.mediator import Mediator
from domain.interfaces.message_broker import BaseMessageBroker


async def init_message_broker():
    container = init_container()
    message_broker = await container.get(BaseMessageBroker)
    await message_broker.start()


async def consume_in_background():
    container = init_container()
    message_broker = await container.get(BaseMessageBroker)

    mediator = await container.get(Mediator)

    async for message in message_broker.start_consuming(settings.message_broker.topic):
        # TO-DO mediator handle event
        await mediator.handle_event(message)


async def close_message_broker():
    container = init_container()
    message_broker = await container.get(BaseMessageBroker)

    await message_broker.close()
