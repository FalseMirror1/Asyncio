import asyncio
import config

from sqlalchemy import Integer, String, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


engine = create_async_engine(config.db_link)
Base = declarative_base()


class CharacterModel(Base):
    __tablename__ = 'Character'

    id = Column(Integer, primary_key=True)
    birth_year = Column(String())
    eye_color = Column(String())
    films = Column(String())
    gender = Column(String())
    hair_color = Column(String())
    height = Column(String())
    homeworld = Column(String())
    mass = Column(String())
    name = Column(String())
    species = Column(String())
    skin_color = Column(String())
    starships = Column(String())
    vehicles = Column(String())


async def get_async_session(drop: bool = False, create: bool = False):
    async with engine.begin() as conn:
        if drop:
            print('Dropped')
            await conn.run_sync(Base.metadata.drop_all)
        if create:
            print('Created')
            await conn.run_sync(Base.metadata.create_all)
    async_session_maker = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )
    return async_session_maker


async def session_create():
    await get_async_session(True, True)


if __name__ == '__main__':
    asyncio.run(session_create())