#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/6/27 20:44
# @File           : PicUtil.py
# @IDE            : PyCharm
# @desc           : 简要说明
import base64

import requests
from fastapi import UploadFile
from redis.asyncio import Redis


class PicUtil:

    def __init__(self, rd: Redis):
        """
        初始化微信认证
        :param index: 选择小程序，0：微信服务端
        """
        # 重试次数
        self.rd = rd


    async def uploadFile_to_base64(self, file_content: UploadFile) -> str:
        # 读取文件内容为二进制
        file_bytes = await file_content.read()
        # 编码为 base64 字符串
        base64_str = base64.b64encode(file_bytes).decode("utf-8")
        return base64_str