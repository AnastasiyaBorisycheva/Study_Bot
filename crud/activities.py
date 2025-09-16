from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from crud.base import CRUDBase
from database.models import Activity, Activity_Subtype


class ActivityCRUD(CRUDBase):

    def __init__(self):
        super().__init__(Activity)

    async def get_activities_list_by_telegram_id(
            self,
            telegram_id: int,
            session: AsyncSession,
            skip: int = 0,
            limit: int = 10
    ):
        activities_list = await session.execute(
            select(Activity).where(
                Activity.telegram_id == telegram_id
            ).options(
                selectinload(Activity.activity_subtype)
                .selectinload(Activity_Subtype.activity_type)
            ).order_by(
                Activity.activity_date
            ).offset(skip).limit(limit)
        )
        return activities_list.scalars().all()


activity_crud = ActivityCRUD()
