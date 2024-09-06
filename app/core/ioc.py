from functools import lru_cache

from dishka import AsyncContainer, make_async_container

from .providers import MyProvider, SqlRepositoryProvider, DatabaseProvider


@lru_cache(1)
def init_container() -> AsyncContainer:
    return make_async_container(
        MyProvider(), SqlRepositoryProvider(), DatabaseProvider()
    )
