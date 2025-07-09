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
    async def call_llm(self, file: UploadFile, user_id: Integer) -> SuccessResponse:

        await file.seek(0)
        client = OpenAI(
            api_key=INTERNLM3_API_KEY,  # 此处传token，不带Bearer
            base_url=INTERNLM3_BASE_URL,
        )

        # 创建 PicUtil 实例
        pic_util = PicUtil(rd=self.rd)
        image_base64 = await pic_util.uploadFile_to_base64(file)

        # Prompt 模板
        prompt_template = """{
          "task_description": "识别图片中的中小学考试题目，提取题目内容、问题类型和关键信息",
          "input_requirements": "包含完整题目的清晰图片，支持数学、语文、英语、科学等学科",
          "response_format": {
            "code": "enum[200, 300, 400, 500]",
            "message": "string",            
            "data": {
              "question_content": "string",
              "subject": "enum['数学', '语文', '英语', '科学', '物理', '化学', '生物', '历史', '地理', '政治']",
              "question_type": "enum['选择题', '填空题', '解答题', '判断题', '应用题', '阅读理解', '作文题']",
              "difficulty": "enum['基础', '中等', '较难', '困难']",
              "keywords": ["string"],
              "answer_position": {
                "exists": "boolean",
                "coordinates": "array[left, top, right, bottom]（若存在）"
              },
              "solution_steps": "string（若图片中存在）",
              "special_requirements": "string（如：保留两位小数、用中文作答等）"
            }
          },
          "status_codes": {
            "200": "成功识别中小学考试题目",
            "300": "识别成功，但内容非中小学考试题目",
            "400": "输入不符合要求（如图片模糊、不完整等）",
            "500": "系统处理错误"
          },
          "example_success": {
            "code": 200, 
            "message": "识别成功",
            "data": {
              "question_content": "小明有5个苹果，小红比小明多3个，请问小红有几个苹果？",
              "subject": "数学",
              "question_type": "应用题",
              "difficulty": "基础",
              "keywords": ["苹果", "数量", "加法"],
              "answer_position": {"exists": false},
              "solution_steps": "",
              "special_requirements": ""
            }
          },
          "example_error": {
            "code": 300, 
            "message": "识别内容非中小学考试题目",
            "data": null
          },
          "cautions": [
            "忽略图片中的装饰元素和无关文字",
            "对于选择题，需提取所有选项内容",
            "识别公式和符号时，使用LaTeX格式表示（如：\\frac{1}{2} 表示二分之一）",
            "若题目跨页，需分别标注每张图片的内容"
          ]
        }"""
        # 构建请求（图 + 文）
        response = client.chat.completions.create(
            model="internvl3-latest",  # 注意：模型名必须是服务支持的
            messages=[
                {
                    "role": "user",
                    "content": [
                        # 将提示词动态化，配置在字典表中
                        # {"type": "text", "text": "请分析这张图片"},
                        {"type": "text", "text": prompt_template},
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
        # 写入数据表

        return SuccessResponse(data=response.choices[0].message.content)




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













