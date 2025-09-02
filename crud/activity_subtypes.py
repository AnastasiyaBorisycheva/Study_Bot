from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import CRUDBase
from database.models import Activity_Subtype


class ActivitySubTypeCRUD(CRUDBase):

    def __init__(self):
        super().__init__(Activity_Subtype)

    async def get_subtypes_by_activite(self, session: AsyncSession, activity_type_id: int):
        result = await session.execute(
            select(Activity_Subtype).where(Activity_Subtype.activity_type_id == activity_type_id)
        )
        return result.scalars().all()


activity_subtype_crud = ActivitySubTypeCRUD()
