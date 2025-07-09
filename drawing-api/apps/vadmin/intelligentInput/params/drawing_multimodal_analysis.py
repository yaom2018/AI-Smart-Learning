#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/07/09 17:27
# @File           : drawing_multimodal_analysis.py
# @IDE            : PyCharm
# @desc           : 多模态分析结果表

from fastapi import Depends
from core.dependencies import Paging, QueryParams


class DrawingMultimodalAnalysisParams(QueryParams):
    def __init__(self, params: Paging = Depends()):
        super().__init__(params)
