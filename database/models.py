from database.database import Base
from sqlalchemy import Column, Integer, String, Boolean


class Todos(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)


class Second(Base):

    __tablename__ = "second"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(String)
    complete = Column(Boolean, default=False)
