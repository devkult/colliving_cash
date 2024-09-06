from contextlib import asynccontextmanager
from dishka import AsyncContainer
from fastapi import FastAPI
from aiojobs import Scheduler
from dishka.integrations.fastapi import setup_dishka
from presentation.api.lifespan import close_message_broker, consume_in_background
from core.ioc import init_container
from domain.logic.mediator import Mediator
from presentation.api.colliving import router as api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    container = init_container()
    scheduler = await container.get(Scheduler)
    mediator = await container.get(Mediator)
    
    # job = await scheduler.spawn(consume_in_background())

    yield
    # await job.close()
    await close_message_broker()
    await app.state.dishka_container.close()


def create_app(container: AsyncContainer = init_container()) -> FastAPI:
    app = FastAPI(
        title="CollivingCash",
        description="CollivingCash API",
        docs_url="/api/docs",
        version="1.0.0",
        debug=True,
        lifespan=lifespan,
    )

    app.include_router(api_router, prefix="/api")

    setup_dishka(container, app)

    return app
