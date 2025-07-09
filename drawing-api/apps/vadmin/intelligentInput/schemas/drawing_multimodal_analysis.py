#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/07/09 17:27
# @File           : drawing_multimodal_analysis.py
# @IDE            : PyCharm
# @desc           : pydantic 模型，用于数据库序列化操作

from pydantic import BaseModel, Field, ConfigDict
from core.data_types import DatetimeStr


class DrawingMultimodalAnalysis(BaseModel):
    image_id: str = Field(..., title="关联图片ID")
    analysis_type: str = Field(..., title="分析类型")
    analysis_result: dict = Field(..., title="分析结果（JSON格式）")
    llm_model: str = Field(..., title="使用的LLM模型")
    confidence: float = Field(..., title="分析置信度（0-1）")
    analysis_time: datetime = Field(..., title="分析时间")
    create_user_id: int = Field(..., title="创建用户ID")


class DrawingMultimodalAnalysisSimpleOut(DrawingMultimodalAnalysis):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., title="编号")
    create_datetime: DatetimeStr = Field(..., title="创建时间")
    update_datetime: DatetimeStr = Field(..., title="更新时间")
