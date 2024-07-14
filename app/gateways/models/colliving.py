from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    uuid = Column(String, primary_key=True)

class House(Base):
    __tablename__ = "houses"
    name = Column(String)
    owner_uuid = Column(String)

