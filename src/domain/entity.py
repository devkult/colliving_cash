from dataclasses import dataclass, field
from datetime import datetime
from random import randint


from .exc import UserNotFoundException


@dataclass(kw_only=True)
class BaseEntity:
    id: int = field(default_factory=lambda: randint(1, 1000))


@dataclass()
class User(BaseEntity):
    name: str = "User"

    def __hash__(self) -> int:
        return hash(self.name)


@dataclass
class Bill(BaseEntity):
    amount: int
    title: str
    description: str
    date: datetime = field(default_factory=datetime.now)


@dataclass
class Home(BaseEntity):
    name: str
    users: list[User] = field(default_factory=list)
    bills: dict[User : list[Bill]] = field(default_factory=dict)

    def register_bill(self, user: User, bill: Bill) -> Bill:
        if user not in self.bills:
            self.bills[user] = []
        self.bills[user].append(bill)

    def register_user(self, user: User) -> User:
        if user not in self.users:
            self.users.append(user)
        return user


@dataclass
class HomeService:
    def create_home(self, name: str) -> Home:
        return Home(name=name)

    def add_bill(
        self,
        home: Home,
        user: User,
        amount: int,
        title: str = "Unnamed",
        description: str = "",
    ) -> Bill:
        if user not in home.users:
            raise UserNotFoundException(username=user.name)
        return home.register_bill(
            user=user, bill=Bill(amount=amount, title=title, description=description)
        )

    def add_user(self, home: Home, name: str) -> User:
        user = User(name=name)
        home.register_user(user=user)
        return user
