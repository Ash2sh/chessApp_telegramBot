from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from bot.config import dbUrl

Base = declarative_base()

def create_pool() -> sessionmaker:
    engine: Engine = create_async_engine(dbUrl)
    pool: sessionmaker = sessionmaker(class_=AsyncSession, autocommit=False, expire_on_commit=False, autoflush=False, bind=engine)

    return pool