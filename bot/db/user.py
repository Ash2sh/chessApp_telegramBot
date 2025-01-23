from sqlalchemy import Column, Integer, String

from .base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    firstSurName = Column(String)
    birthYear = Column(Integer)
    sex = Column(String)
    ageCategory = Column(String)
    ratingFIDE = Column(Integer)
    classRank = Column(Integer)
    innPin = Column(String)
    сriteria = Column(String)
    status = Column(String)