from dataclasses import dataclass, field
from typing import Any, DefaultDict, Dict, Iterable, Type

from dishka import AsyncContainer

from domain.logic.commands.base import CR, CT, BaseCommand, BaseCommandHandler
from domain.logic.queries.base import QR, BaseQuery, BaseQueryHandler


@dataclass(kw_only=True)
class Mediator:
    commands_map: dict[Type[CT], list[BaseCommandHandler]] = field(
        default_factory=lambda: DefaultDict(list)
    )
    queries_map: Dict[Type[BaseQuery[Any]], BaseQueryHandler[Any]] = field(
        default_factory=dict
    )

    container: AsyncContainer

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

    def register_query(
        self, query_type: Type[BaseQuery[QR]], handler: BaseQueryHandler[QR]
    ) -> None:
        self.queries_map[query_type] = handler

    async def handle_query(self, query: BaseQuery[QR]) -> QR:
        handler_class = self.queries_map.get(type(query))
        async with self.container() as container_r:
            handler: BaseQueryHandler[QR] = await container_r.get(handler_class)
            return await handler.handle(query)
