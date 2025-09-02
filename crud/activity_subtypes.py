from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import CRUDBase
from database.models import Activity_Subtype


class ActivitySubTypeCRUD(CRUDBase):

    def __init__(self, model):
        super().__init__(Activity_Subtype)


activity_type_crud = ActivitySubTypeCRUD()
