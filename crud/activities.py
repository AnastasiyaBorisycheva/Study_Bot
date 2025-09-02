from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import CRUDBase
from database.models import Activity


class ActivityCRUD(CRUDBase):

    def __init__(self):
        super().__init__(Activity)


activity_crud = ActivityCRUD()
