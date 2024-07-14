from contextlib import asynccontextmanager
from fastapi import FastAPI
from dishka.integrations.fastapi import setup_dishka
from logic.init import init_container
from logic.mediator import Mediator


@asynccontextmanager
async def lifespan(app: FastAPI):
    container = init_container()
    mediator = await container.get(Mediator)
    mediator.container = container

    yield

    await app.state.dishka_container.close()


def create_app() -> FastAPI:
    app = FastAPI(
        title="CollivingCash",
        description="CollivingCash API",
        version="1.0.0",
        debug=True,
        lifespan=lifespan,
    )

    container = init_container()
    setup_dishka(container, app)
    return app
