#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/7/9 13:41
# @File           : DrawingMultimodalAnalysis.py
# @IDE            : PyCharm
# @desc           : 多模态分析结果表

from sqlalchemy.orm import relationship, Mapped, mapped_column
from apps.vadmin.auth.models import VadminUser
from db.db_base import BaseModel
from sqlalchemy import String, ForeignKey, Integer, DateTime, Float, Boolean, Enum, JSON
from datetime import datetime


class DrawingMultimodalAnalysis(BaseModel):
    __tablename__ = "drawing_multimodal_analysis"
    __table_args__ = ({'comment': '多模态分析结果表'})


    image_id: Mapped[str] = mapped_column(
        String(36),
        nullable=False,
        comment='关联图片ID'
    )

    analysis_type: Mapped[str] = mapped_column(
        Enum('caption', 'qa', 'classification', 'scene', 'object_detection', name='analysis_type_enum'),
        nullable=False,
        comment='分析类型'
    )

    analysis_result: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
        comment='分析结果（JSON格式）'
    )

    llm_model: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment='使用的LLM模型'
    )

    confidence: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        comment='分析置信度（0-1）'
    )

    analysis_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default="CURRENT_TIMESTAMP(3)",
        comment='分析时间'
    )

    create_user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("vadmin_auth_user.id", ondelete='RESTRICT'),
        nullable=False,
        comment='创建用户ID'
    )

    create_datetime: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default="CURRENT_TIMESTAMP",
        comment='创建时间'
    )

    update_datetime: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default="CURRENT_TIMESTAMP",
        onupdate="CURRENT_TIMESTAMP",
        comment='更新时间'
    )

    delete_datetime: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True,
        comment='删除时间'
    )

    is_delete: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        comment='是否软删除'
    )

    create_user: Mapped[VadminUser] = relationship(foreign_keys=create_user_id)