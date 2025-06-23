#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2023/8/25 13:41
# @File           : DrawingImages.py
# @IDE            : PyCharm
# @desc           : 图片素材表

from sqlalchemy.orm import relationship, Mapped, mapped_column
from apps.vadmin.auth.models import VadminUser
from db.db_base import BaseModel
from sqlalchemy import String, ForeignKey, Integer, BigInteger, Text, Boolean


class DrawingImagesRecord(BaseModel):
    __tablename__ = "drawing_resource_images"
    __table_args__ = ({'comment': '上传图片素材表'})

    filename: Mapped[str] = mapped_column(String(255), nullable=False, comment="原图片名称")

    # 图片链接
    image_url: Mapped[str] = mapped_column(Text, nullable=False, comment="图片链接")

    # 文件大小（单位：字节）
    file_size: Mapped[int] = mapped_column(BigInteger, nullable=False, comment="文件大小（字节）")

    # 图片类型（如 jpg, png, gif 等）
    image_type: Mapped[str] = mapped_column(String(50), nullable=False, comment="图片类型")

    # 图片宽度（像素）
    width: Mapped[int] = mapped_column(Integer, nullable=True, comment="图片宽度（像素）")

    # 图片高度（像素）
    height: Mapped[int] = mapped_column(Integer, nullable=True, comment="图片高度（像素）")

    # 是否公开访问
    is_public: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, comment="是否公开访问")

    # 图片描述
    description: Mapped[str] = mapped_column(Text, nullable=True, comment="图片描述")

    # 标签（JSON 格式存储）
    tags: Mapped[str] = mapped_column(Text, nullable=True, comment="图片标签（JSON 格式）")

    create_user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("vadmin_auth_user.id", ondelete='RESTRICT'),
        comment="创建人"
    )
    create_user: Mapped[VadminUser] = relationship(foreign_keys=create_user_id)
