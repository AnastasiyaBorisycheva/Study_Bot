from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import CRUDBase
from database.models import Activity


class ActivityCRUD(CRUDBase):

    def __init__(self):
        super().__init__(Activity)

    async def get_activities_list_by_telegram_id(
            self,
            telegram_id: int,
            session: AsyncSession,
    ):
        activities_list = await session.execute(
            select(Activity).where(
                Activity.telegram_id == telegram_id
            ).order_by(
                desc(Activity.activity_date))
        )
        return activities_list.scalars().all()


activity_crud = ActivityCRUD()
