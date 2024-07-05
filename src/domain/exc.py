from dataclasses import dataclass


@dataclass(frozen=True)
class ColivingCashException(Exception):
    @property
    def message(self) -> str:
        return f"Ошибка на уровне приложения"


@dataclass(frozen=True)
class UserNotFoundException(ColivingCashException):
    username: str

    @property
    def message(self) -> str:
        return f"Пользователь {self.username} не найден"
