# viewsCheckService.py
from sqlalchemy import Integer

from utils.llm.picUtil import PicUtil
from utils.response import SuccessResponse, ErrorResponse
from fastapi import  UploadFile
from PIL import Image
from io import BytesIO
import hashlib
import mimetypes
from redis.asyncio import Redis
from application.settings import REDIS_VALID_TIME, INTERNLM3_API_KEY, INTERNLM3_BASE_URL
from openai import OpenAI

class ViewsCheckService:
    """
    服务类：用于校验图片有效性、幂等性检查等操作。
    """

    def __init__(self, rd: Redis):
        """
        初始化服务类。
        :param redis_client: Redis 客户端实例，用于幂等性检查。
        """
        self.rd = rd
        print(f"Redis client initialized: {self.rd}")

    # 调用多模态接口处理图片内容
    async def call_llm(self, file_content: UploadFile, user_id: Integer) -> SuccessResponse:


        client = OpenAI(
            api_key=INTERNLM3_API_KEY,  # 此处传token，不带Bearer
            base_url=INTERNLM3_BASE_URL,
        )

        # 创建 PicUtil 实例
        pic_util = PicUtil(rd=self.rd)
        image_base64 = await pic_util.uploadFile_to_base64(file_content)

        # 构建请求（图 + 文）
        response = client.chat.completions.create(
            model="internvl3-latest",  # 注意：模型名必须是服务支持的
            messages=[
                {
                    "role": "user",
                    "content": [
                        # 将提示词动态化，配置在字典表中
                        {"type": "text", "text": "请分析这张图片"},
                        {"type": "image_url", "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}"
                        }}
                    ]
                }
            ],
            temperature=0.7,
            top_p=0.9,
        )

        print(response.choices[0].message.content)
        return SuccessResponse(data=response.choices[0].message.content)


        # try:
        #     # 上传图片
        #     upload_response = client.files.create(
        #         file=(file_content.filename, file_content.file),
        #         purpose="assistants"
        #     )
        #
        #     # 获取上传后的文件ID
        #     file_id = upload_response.id
        #
        #     # 发送聊天请求
        #     chat_rsp = client.chat.completions.create(
        #         model="internvl3-latest",
        #         messages=[
        #             {
        #                 "role": "user",
        #                 "content": [
        #                     {"type": "text", "text": "请返回这张图片的内容"},
        #                     {"type": "image", "image": {"file_id": file_id}}
        #                 ]
        #             }
        #         ]
        #     )
        #
        #     # 处理返回的响应
        #     if chat_rsp.choices and len(chat_rsp.choices) > 0:
        #         response_message = chat_rsp.choices[0].message
        #         if response_message.content:
        #             return {"response": response_message.content}
        #         else:
        #             return {"error": "助手没有回复内容。"}
        #     else:
        #         return {"error": "未收到任何回复。"}
        # except Exception as e:
        #     return {"error": f"处理图片时发生错误: {str(e)}"}


    async def check_image_validity(self, file: UploadFile) -> SuccessResponse:
        """
        校验图片的有效性。
        :param file: 上传的文件对象。
        :return: 如果校验通过，返回文件内容（字节流）。
        """
        # 读取文件内容
        file_content = await file.read()

        try:
            # 校验文件是否为空
            if len(file_content) == 0:
                return ErrorResponse(msg="文件为空，请上传有效文件", code=400)

            # 校验文件大小（限制为 5MB）
            MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
            if len(file_content) > MAX_FILE_SIZE:
                return ErrorResponse(msg="文件过大，最大允许上传 5MB", code=400)

            # 校验文件 MIME 类型
            mime_type, _ = mimetypes.guess_type(file.filename)
            if not mime_type or not mime_type.startswith("image"):
                return ErrorResponse(msg="文件不是图片类型", code=400)

            # 使用 Pillow 验证图片格式
            try:
                image = Image.open(BytesIO(file_content))
                image.verify()  # 验证图片完整性
                print(f"图片尺寸: {image.size}")  # 输出图片宽度和高度
            except Exception as e:
                return ErrorResponse(msg="无效的图片文件", code=400)

            return SuccessResponse(data=file_content)
        except Exception as e:

            return ErrorResponse(msg=f"系统错误: {str(e)}", code=500)


    async def check_idempotency(self, file_content: bytes, user_id: Integer) -> SuccessResponse:
        """
        幂等性检查。
        :param file_content: 文件内容（字节流）。
        :param user_id: 当前用户的唯一标识。
        :return: 如果 Redis 中存在缓存结果，返回 URL 字符串；否则返回 None。
        """
        # 检查 file_content 是否为 None
        if file_content is None:
            print("file_content 为 None，无法计算哈希值")
            return ErrorResponse(msg=f"文件已上传过，请勿重复上传", code=500)

        # 确保 file_content 是 bytes 类型
        if not isinstance(file_content, bytes):
            try:
                file_content = file_content.encode('utf-8')
            except AttributeError:
                print("无法将 file_content 转换为 bytes 类型")
                return None

        # 计算文件哈希值
        file_hash = hashlib.md5(file_content).hexdigest()
        key = f"uploadfile:{user_id}:{file_hash}"
        value = f"uploadfile:{file_hash}"

        # 检查 Redis 中是否存在该 key
        cached_result = await self.rd.get(key)
        if cached_result:
            print(f"文件已上传过，直接返回缓存结果: {cached_result.decode()}")
            return ErrorResponse(msg=f"文件已上传过，请勿重复上传", code=409)
        else:
            # 如果 Redis 中不存在该 key，则将其存入 Redis 缓存
            await self.rd.set(key, value, ex=REDIS_VALID_TIME)
            print(f"文件未上传过，存入 Redis 缓存: {value}")

        return SuccessResponse(data="上传成功", code=200)

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













