from typing import Protocol


class AsyncUnitOfWork(Protocol):

    async def commit(self):
        pass

    async def rollback(self):
        pass