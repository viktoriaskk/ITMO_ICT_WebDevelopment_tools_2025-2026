"""
Асинхронная обёртка над SQLAlchemy session: select/insert/update/delete и upsert.

Используется во всех core-* модулях; повторные попытки на уровне декоратора retry_async.
"""

from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select, update, delete
from sqlalchemy.sql.functions import func

from typing import Type, TypeVar, Any

from utils.func_utils import retry_async
from models._base_class import Base


ModelType = TypeVar("ModelType", bound=Base)


class DatabaseWorkerAsync:
    def __init__(self, engine) -> None:
        self.engine_async = engine
        self.async_session_maker = async_sessionmaker(
            self.engine_async, expire_on_commit=False
        )

    @retry_async(5)
    async def session_execute(self, stmt) -> list:
        async with self.async_session_maker() as session:
            result = await session.execute(stmt)
            return result.all()

    @retry_async(5)
    async def session_scalars(self, stmt) -> list:
        async with self.async_session_maker() as session:
            result = await session.scalars(stmt)
            return result.all()

    @retry_async(5)
    async def session_execute_commit(self, stmt) -> None:
        async with self.async_session_maker() as session:
            await session.execute(stmt)
            await session.commit()

    @retry_async(5)
    async def session_scalars_commit(self, stmt) -> list:
        async with self.async_session_maker() as session:
            result = await session.scalars(stmt)
            await session.commit()
            return result.all()

    async def custom_orm_select(
        self,
        cls_from: list[Type[ModelType]] | Type[ModelType] | Any,
        select_from: list = None,
        join_on: list = None,
        outerjoin_on: list = None,
        where_params: list = None,
        sql_limit: int = None,
        offset: int = None,
        order_by: list = None,
        group_by: list = None,
        distinct: bool = None,
        return_unpacked: bool = False,
    ) -> Type[ModelType] | list[Type[ModelType]] | Any:
        stmt = select(*cls_from) if isinstance(cls_from, list) else select(cls_from)

        if select_from:
            stmt = (
                stmt.select_from(*select_from)
                if isinstance(select_from, list)
                else stmt.select_from(select_from)
            )

        if join_on:
            for join in join_on:
                stmt = stmt.join(*join)

        if outerjoin_on:
            for outerjoin in outerjoin_on:
                stmt = stmt.outerjoin(*outerjoin)

        if where_params:
            stmt = stmt.where(*where_params)

        if sql_limit:
            stmt = stmt.limit(sql_limit)

        if offset:
            stmt = stmt.offset(offset)

        if order_by:
            stmt = stmt.order_by(*order_by)

        if group_by:
            stmt = stmt.group_by(*group_by)

        if distinct:
            stmt = stmt.distinct()

        if isinstance(cls_from, list):
            result = await self.session_execute(stmt)
        else:
            result = await self.session_scalars(stmt)

        return result[0] if len(result) == 1 and return_unpacked else result

    @retry_async(5)
    async def custom_orm_bulk_update(self, cls_to: Type[ModelType], data: list) -> None:
        async with self.async_session_maker() as session:
            await session.execute(update(cls_to), data)
            await session.commit()

    async def custom_insert_do_nothing(
        self,
        cls_to: Type[ModelType],
        index_elements: list,
        data: list,
        returning: Type[ModelType] = None,
        return_unpacked: bool = False,
    ) -> Type[ModelType] | list[Type[ModelType]] | Any:
        stmt = (
            insert(cls_to)
            .values(data)
            .on_conflict_do_nothing(index_elements=index_elements)
        )
        if returning:
            stmt = stmt.returning(returning)
            result = await self.session_scalars_commit(stmt)
            return result[0] if return_unpacked and len(result) == 1 else result
        await self.session_execute_commit(stmt)

    async def custom_upsert(
        self,
        cls_to: Type[ModelType],
        index_elements: list,
        data: list,
        update_set: list,
        returning: Type[ModelType] = None,
        return_unpacked: bool = False,
    ) -> Type[ModelType] | list[Type[ModelType]] | Any:
        stmt = insert(cls_to).values(data)
        stmt = stmt.on_conflict_do_update(
            index_elements=index_elements,
            set_={x: getattr(stmt.excluded, x) for x in update_set},
        )
        if returning:
            stmt = stmt.returning(returning)
            result = await self.session_scalars_commit(stmt)
            return result[0] if return_unpacked and len(result) == 1 else result
        await self.session_execute_commit(stmt)

    async def custom_insert(
        self,
        cls_to: Type[ModelType],
        data: list,
        returning: Type[ModelType] = None,
        return_unpacked: bool = False,
    ) -> Type[ModelType] | list[Type[ModelType]] | Any:
        stmt = insert(cls_to).values(data)
        if returning:
            stmt = stmt.returning(returning)
            result = await self.session_scalars_commit(stmt)
            return result[0] if return_unpacked and len(result) == 1 else result
        await self.session_execute_commit(stmt)

    async def custom_update(
        self,
        cls_to: Type[ModelType],
        data: dict,
        where_params: list,
        returning: Type[ModelType] = None,
        return_unpacked: bool = False,
    ) -> Type[ModelType] | Any:
        stmt = update(cls_to).where(*where_params).values(**data)
        if returning:
            stmt = stmt.returning(returning)
            result = await self.session_scalars_commit(stmt)
            return result[0] if return_unpacked and len(result) == 1 else result
        await self.session_execute_commit(stmt)

    async def custom_delete_all(
        self, cls_from: Type[ModelType], where_params: list = None
    ) -> None:
        stmt = delete(cls_from)
        if where_params:
            stmt = stmt.where(*where_params)
        await self.session_execute_commit(stmt)

    async def count(
        self,
        cls_from: Type[ModelType],
        where_params: list = None,
        join_on: list = None,
        outerjoin_on: list = None,
        distinct_on: Type[ModelType] = None,
    ) -> int:

        if distinct_on:
            stmt = select(func.count(func.distinct(distinct_on.id)))
        else:
            stmt = select(func.count())

        stmt = stmt.select_from(cls_from)

        if join_on:
            for join in join_on:
                stmt = stmt.join(*join)

        if outerjoin_on:
            for outerjoin in outerjoin_on:
                stmt = stmt.outerjoin(*outerjoin)

        if where_params:
            stmt = stmt.where(*where_params)

        async with self.async_session_maker() as session:
            result = await session.scalar(stmt)
            return [result] if result is not None else [0]
