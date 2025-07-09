#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/06/22 16:46
# @File           : crud.py
# @IDE            : PyCharm
# @desc           : 数据访问层
from core.crud import DalBase
from . import models, schemas
from sqlalchemy.ext.asyncio import AsyncSession




class DrawingImagesRecordDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(DrawingImagesRecordDal, self).__init__()
        self.db = db
        self.model = models.DrawingImagesRecord
        self.schema = schemas.DrawingImagesRecordSimpleOut


class DrawingImagesRecordDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(DrawingImagesRecordDal, self).__init__()
        self.db = db
        self.model = models.DrawingImagesRecord
        self.schema = schemas.DrawingImagesRecordSimpleOut




class DrawingMultimodalAnalysisDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(DrawingMultimodalAnalysisDal, self).__init__()
        self.db = db
        self.model = models.DrawingMultimodalAnalysis
        self.schema = schemas.DrawingMultimodalAnalysisSimpleOut
