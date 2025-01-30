from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, Session, declarative_base

import asyncio

from bot.config import dbUrl

Base = declarative_base()

def create_pool() -> sessionmaker:
    engine: Engine = create_async_engine(dbUrl)
    pool: sessionmaker = sessionmaker(class_=AsyncSession, autocommit=False, expire_on_commit=False, autoflush=False, bind=engine)

    return pool

from sqlalchemy import Column, Integer, String

class Test(Base):
    __tablename__ = "test"

    id = Column(Integer, primary_key=True, index=True, unique=True)

async def main():
    db:Session = create_pool()()
    dbUser = Test(id=1)
    db.add(dbUser)
    await db.commit()

asyncio.run(main())