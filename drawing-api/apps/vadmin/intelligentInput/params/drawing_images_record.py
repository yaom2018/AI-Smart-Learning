#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/06/22 16:52
# @File           : drawing_images_record.py
# @IDE            : PyCharm
# @desc           : AI智慧上传图片

from fastapi import Depends
from core.dependencies import Paging, QueryParams


class DrawingImagesRecordParams(QueryParams):
    def __init__(self, params: Paging = Depends()):
        super().__init__(params)
