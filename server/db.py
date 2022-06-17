from typing import AsyncGenerator, Any
from fastapi import HTTPException, status
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from server.config import config


metadata = sqlalchemy.MetaData()

engine = create_async_engine(
    config.DATABASE_URL,
    future=True,
    echo=True,
)

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


@as_declarative()
class Base:
    id: Any
    is_deleted: bool
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__

    @classmethod
    async def get_by_id(cls, obj_id: int, db_session: AsyncSession, ignore_none=False):
        """Get object instance from database selected by ID
        :param obj_id: id of looking instance
        :param db_session:
        :param ignore_none: if False will raise HTTPException if result is None
        :return:
        """
        query = select(cls).where(cls.id == obj_id)
        result = await db_session.execute(query)
        instance = result.scalar()
        if instance is None and not ignore_none:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Model don't exists")
        return instance

    async def save(self, db_session: AsyncSession, commit: bool = True):
        try:
            db_session.add(self)
            if commit:
                return await db_session.commit()
        except SQLAlchemyError as ex:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=repr(ex))


async def get_db() -> AsyncGenerator:
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except SQLAlchemyError as sql_ex:
            await session.rollback()
            raise sql_ex
        except HTTPException as http_ex:
            await session.rollback()
            raise http_ex
        finally:
            await session.close()
