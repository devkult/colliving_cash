from dataclasses import dataclass, field
from typing import DefaultDict, Iterable

from dishka import AsyncContainer

from domain.logic.commands.base import CR, CT, BaseCommand, BaseCommandHandler
from domain.logic.queries.base import QR, BaseQuery, BaseQueryHandler


@dataclass(kw_only=True)
class Mediator:
    commands_map: dict[CT, list[BaseCommandHandler]] = field(
        default_factory=lambda: DefaultDict(list)
    )
    queries_map: dict[CT, BaseQueryHandler] = field(
        default_factory=lambda: DefaultDict(list)
    )

    container: AsyncContainer = None

    def register_command(
        self, command: CT, handlers: Iterable[BaseCommandHandler[CT, CR]]
    ) -> None:
        self.commands_map[command].extend(handlers)

    async def handle_command(self, command: BaseCommand) -> Iterable[CR]:
        command_type = type(command)

        async with self.container() as container_r:
            handlers: Iterable[BaseCommandHandler] = [
                await container_r.get(handler)
                for handler in self.commands_map.get(command_type)
            ]
            return [await handler.handle(command) for handler in handlers]

    def register_query(self, query: CT, handler: BaseQueryHandler[CT, QR]) -> None:
        self.queries_map[query] = handler

    async def handle_query(self, query: BaseQuery) -> QR:
        query_type = type(query)

        async with self.container() as container_r:
            handler: BaseQueryHandler = await container_r.get(
                self.queries_map.get(query_type)
            )
            return await handler.handle(query)
