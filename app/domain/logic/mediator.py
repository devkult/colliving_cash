from dataclasses import dataclass, field
from typing import DefaultDict, Iterable

from dishka import AsyncContainer

from domain.logic.commands.base import CR, CT, BaseCommand, CommandHandler


@dataclass(kw_only=True)
class Mediator:
    commands_map: dict[CT, list[CommandHandler]] = field(
        default_factory=lambda: DefaultDict(list)
    )
    container: AsyncContainer = None

    def register_command(
        self, command: CT, handlers: Iterable[CommandHandler[CT, CR]]
    ) -> None:
        self.commands_map[command].extend(handlers)

    async def handle_command(self, command: BaseCommand) -> Iterable[CR]:
        command_type = type(command)
        handlers = self.commands_map.get(command_type)

        async with self.container() as container_r:
            handlers = [await container_r.get(handler) for handler in handlers]
            return [await handler.handle(command) for handler in handlers]
