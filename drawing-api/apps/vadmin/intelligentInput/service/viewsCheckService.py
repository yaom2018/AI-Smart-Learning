# viewsCheckService.py

from fastapi import HTTPException, UploadFile
from PIL import Image
from io import BytesIO
import hashlib
import mimetypes
from typing import Optional
from redis.asyncio import Redis

class ViewsCheckService:
    """
    服务类：用于校验图片有效性、幂等性检查等操作。
    """

    def __init__(self, redis: Redis):
        """
        初始化服务类。
        :param redis_client: Redis 客户端实例，用于幂等性检查。
        """
        self.redis = redis

    async def check_image_validity(self, file: UploadFile) -> bytes:
        """
        校验图片的有效性。
        :param file: 上传的文件对象。
        :return: 如果校验通过，返回文件内容（字节流）。
        """
        # 读取文件内容
        file_content = await file.read()

        # 校验文件是否为空
        if len(file_content) == 0:
            raise HTTPException(status_code=400, detail="文件为空，请上传有效文件。")

        # 校验文件大小（限制为 5MB）
        MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
        if len(file_content) > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail="文件过大，最大允许上传 5MB。")

        # 校验文件 MIME 类型
        mime_type, _ = mimetypes.guess_type(file.filename)
        if not mime_type or not mime_type.startswith("image"):
            raise HTTPException(status_code=400, detail="文件不是图片类型。")

        # 使用 Pillow 验证图片格式
        try:
            image = Image.open(BytesIO(file_content))
            image.verify()  # 验证图片完整性
            print(f"图片尺寸: {image.size}")  # 输出图片宽度和高度
        except Exception as e:
            raise HTTPException(status_code=400, detail="无效的图片文件。")

        return file_content

    async def check_idempotency(self, file_content: bytes, user_id: str) -> Optional[str]:
        """
        幂等性检查。
        :param file_content: 文件内容（字节流）。
        :param user_id: 当前用户的唯一标识。
        :return: 如果 Redis 中存在缓存结果，返回 URL 字符串；否则返回 None。
        """
        # 计算文件哈希值
        file_hash = hashlib.md5(file_content).hexdigest()
        key = f"upload:file:{user_id}:{file_hash}"

        # 检查 Redis 中是否存在该 key
        cached_result = self.redis.get(key)
        if cached_result:
            print(f"文件已上传过，直接返回缓存结果: {cached_result.decode()}")
            return cached_result.decode()

        return None

    async def cache_upload_result(self, file_content: bytes, user_id: str, file_url: str, expire_seconds: int = 86400):
        """
        将上传结果存入 Redis 缓存。
        :param file_content: 文件内容（字节流）。
        :param user_id: 当前用户的唯一标识。
        :param file_url: 文件的访问 URL。
        :param expire_seconds: 缓存过期时间（默认 24 小时）。
        """
        file_hash = hashlib.md5(file_content).hexdigest()
        key = f"upload:file:{user_id}:{file_hash}"
        self.redis.set(key, file_url, ex=expire_seconds)