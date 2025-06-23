#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/06/22 16:46
# @File           : crud.py
# @IDE            : PyCharm
# @desc           : 数据访问层
from sqlalchemy.ext.asyncio import AsyncSession
from core.crud import DalBase
from . import schemas, models




class DrawingImagesRecordDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(DrawingImagesRecordDal, self).__init__()
        self.db = db
        self.model = models.DrawingImagesRecord
        self.schema = schemas.DrawingImagesRecordSimpleOut
