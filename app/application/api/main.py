from contextlib import asynccontextmanager
from fastapi import FastAPI
from dishka.integrations.fastapi import setup_dishka
from dependencies.ioc import init_container
from domain.logic.mediator import Mediator
from application.api.colliving import router as api_router


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
        docs_url="/api/docs",
        version="1.0.0",
        debug=True,
        lifespan=lifespan,
    )

    app.include_router(api_router, prefix="/api")

    container = init_container()
    setup_dishka(container, app)

    return app
