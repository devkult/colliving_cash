from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, DeclarativeBase


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    uuid = Column(String, primary_key=True)
    name = Column(String)
    houses = relationship("House", back_populates="owner")
    residents = relationship("Resident", back_populates="user")

class House(Base):
    __tablename__ = "houses"
    uuid = Column(String, primary_key=True)
    name = Column(String)
    owner_uuid = Column(String, ForeignKey('users.uuid'))
    owner = relationship("User", back_populates="houses")
    rooms = relationship("Room", back_populates="house")

class Room(Base):
    __tablename__ = "rooms"
    uuid = Column(String, primary_key=True)
    name = Column(String)
    house_uuid = Column(String, ForeignKey('houses.uuid'))
    house = relationship("House", back_populates="rooms")
    residents = relationship("Resident", back_populates="room")
    capacity = Column(Integer)

class Resident(Base):
    __tablename__ = "residents"
    uuid = Column(String, primary_key=True)
    user_uuid = Column(String, ForeignKey('users.uuid'))
    room_uuid = Column(String, ForeignKey('rooms.uuid'))
    user = relationship("User", back_populates="residents")
    room = relationship("Room", back_populates="residents")
