#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/06/24 17:41
# @File           : drawing_images_record.py
# @IDE            : PyCharm
# @desc           : pydantic 模型，用于数据库序列化操作

from pydantic import BaseModel, Field, ConfigDict
from core.data_types import DatetimeStr


class DrawingImagesRecord(BaseModel):
    filename: str = Field(..., title="原图片名称")
    image_url: str = Field(..., title="图片链接")
    file_size: int = Field(..., title="文件大小（字节）")
    image_type: str = Field(..., title="图片类型")
    width: int | None = Field(None, title="图片宽度（像素）")
    height: int | None = Field(None, title="图片高度（像素）")
    is_public: bool = Field(False, title="是否公开访问")
    description: str | None = Field(None, title="图片描述")
    tags: str | None = Field(None, title="图片标签（JSON 格式）")
    create_user_id: int = Field(..., title="创建人")


class DrawingImagesRecordSimpleOut(DrawingImagesRecord):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., title="编号")
    create_datetime: DatetimeStr = Field(..., title="创建时间")
    update_datetime: DatetimeStr = Field(..., title="更新时间")
