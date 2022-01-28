from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, nullable=False)
    message = Column(String, nullable=False)
    time_created = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    #chatroom_id = Column(Integer, ForeignKey("chatrooms.id", onDelete="CASCADE"), nullable=False)

    user = relationship("User")
    #chatroom = relationship("Chatroom")

#class Chatroom(Base):
#    __tablename__ = "chatrooms"
#
#    id = Column(Integer, primary_key=True, nullable=False)
#    time_created = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
#    owner_id = Column(Integer, ForeignKey("users.id", onDelete="CASCADE"), nullable=False)
#
#    owner = relationship("User")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique= True)
    password = Column(String, nullable=False)
    time_created = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
