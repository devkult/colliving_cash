from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, DeclarativeBase


class Base(DeclarativeBase):
    pass

class UserModel(Base):
    __tablename__ = "users"
    uuid = Column(String, primary_key=True)
    name = Column(String)
    houses = relationship("HouseModel", back_populates="owner")
    residents = relationship("ResidentModel", back_populates="user")

class HouseModel(Base):
    __tablename__ = "houses"
    uuid = Column(String, primary_key=True)
    name = Column(String)
    owner_uuid = Column(String, ForeignKey('users.uuid'))
    owner = relationship("UserModel", back_populates="houses")
    rooms = relationship("RoomModel", back_populates="house")

class RoomModel(Base):
    __tablename__ = "rooms"
    uuid = Column(String, primary_key=True)
    name = Column(String)
    house_uuid = Column(String, ForeignKey('houses.uuid'))
    house = relationship("HouseModel", back_populates="rooms")
    residents = relationship("ResidentModel", back_populates="room")
    capacity = Column(Integer)

class ResidentModel(Base):
    __tablename__ = "residents"
    uuid = Column(String, primary_key=True)
    user_uuid = Column(String, ForeignKey('users.uuid'))
    room_uuid = Column(String, ForeignKey('rooms.uuid'))
    user = relationship("UserModel", back_populates="residents")
    room = relationship("RoomModel", back_populates="residents")
