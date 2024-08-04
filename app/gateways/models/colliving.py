from typing import List, Optional
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column
from sqlalchemy import String, ForeignKey


class Base(DeclarativeBase):
    pass


class UserModel(Base):
    __tablename__ = "users"

    uuid: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(String)
    houses: Mapped[List["HouseModel"]] = relationship(
        "HouseModel", back_populates="owner", cascade="all, delete-orphan"
    )
    residents: Mapped[List["ResidentModel"]] = relationship(
        "ResidentModel", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"UserModel(uuid={self.uuid!r}, name={self.name!r})"


class HouseModel(Base):
    __tablename__ = "houses"

    uuid: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(String)
    owner_uuid: Mapped[Optional[str]] = mapped_column(String, ForeignKey("users.uuid"))
    owner: Mapped["UserModel"] = relationship("UserModel", back_populates="houses")
    residents: Mapped[List["ResidentModel"]] = relationship(
        "ResidentModel", back_populates="house", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"HouseModel(uuid={self.uuid!r}, name={self.name!r}, owner_uuid={self.owner_uuid!r})"


class ResidentModel(Base):
    __tablename__ = "residents"

    uuid: Mapped[str] = mapped_column(String, primary_key=True)
    user_uuid: Mapped[Optional[str]] = mapped_column(String, ForeignKey("users.uuid"))
    house_uuid: Mapped[Optional[str]] = mapped_column(String, ForeignKey("houses.uuid"))
    user: Mapped["UserModel"] = relationship("UserModel", back_populates="residents")
    house: Mapped["HouseModel"] = relationship("HouseModel", back_populates="residents")

    def __repr__(self) -> str:
        return f"ResidentModel(uuid={self.uuid!r}, user_uuid={self.user_uuid!r}, house_uuid={self.house_uuid!r})"
