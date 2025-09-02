from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import CRUDBase
from database.models import Activity_Type


class ActivityTypeCRUD(CRUDBase):

    def __init__(self):
        super().__init__(Activity_Type)


activity_type_crud = ActivityTypeCRUD()
