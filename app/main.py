from logic.init import init_container
from logic.mediator import Mediator


async def main() -> None:
    container = init_container()
    mediator = await container.get(Mediator)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
