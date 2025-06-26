# 依赖安装：pip install orjson
import base64

from fastapi.responses import ORJSONResponse as Response
from fastapi import status as http_status
from utils import status as http


class SuccessResponse(Response):
    """
    成功响应
    """
    def __init__(self, data=None, msg="success", code=http.HTTP_SUCCESS, status=http_status.HTTP_200_OK, **kwargs):
        if isinstance(data, bytes):
            # 将 bytes 类型转换为 base64 编码的字符串
            data = base64.b64encode(data).decode('utf-8')
        self.data = {
            "code": code,
            "message": msg,
            "data": data
        }
        self.data.update(kwargs)
        super().__init__(content=self.data, status_code=status)


class ErrorResponse(Response):
    """
    失败响应
    """
    def __init__(self, msg=None, code=http.HTTP_ERROR, status=http_status.HTTP_200_OK, **kwargs):
        self.data = {
            "code": code,
            "message": msg,
            "data": []
        }
        self.data.update(kwargs)
        super().__init__(content=self.data, status_code=status)
