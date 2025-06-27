#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/06/22 16:52
# @File           : views.py
# @IDE            : PyCharm
# @desc           : 路由，视图文件
from core.database import db_getter,redis_getter
from fastapi import APIRouter, UploadFile, Depends
from redis.asyncio import Redis
from utils.response import SuccessResponse
from apps.vadmin.auth.utils.validation.auth import Auth
from sqlalchemy.ext.asyncio import AsyncSession
from . import crud, schemas, params
from utils.file.aliyun_oss import AliyunOSS, BucketConf
from apps.vadmin.intelligentInput.service.viewsCheckService import ViewsCheckService
from application.settings import ALIYUN_OSS, ALIYUN_OSS_INTELIGENT_PATH
from core.dependencies import IdList
from apps.vadmin.auth.utils.current import AllUserAuth, FullAdminAuth


app = APIRouter()


###########################################################
#    AI智慧上传图片
###########################################################
@app.post("/drawing/images/uploadImg", summary="上传图片", tags=["AI智慧上传图片"])
async def upload_images(file: UploadFile, auth: Auth = Depends(FullAdminAuth()), rd: Redis = Depends(redis_getter)):
    # 图片校验
    # 根据实际情况初始化 Redis 客户端
    service = ViewsCheckService(rd)
    ## 获取文件名称
    # 调用异步方法并获取返回值
    check_result = await service.check_image_validity(file)
    # 判断返回的 code 是否为 400
    if hasattr(check_result, 'code') and check_result.code == 400:
        return check_result

    # 获取 file_content
    file_content = None
    if hasattr(check_result, 'data'):
        outer_data = check_result.data
        if isinstance(outer_data, dict) and 'data' in outer_data:
            file_content = outer_data['data']
            # print(f"从 data 中获取到的值: {file_content}")
        else:
            print("返回结果的 data 属性下不包含 data 字段")
    else:
        print("返回结果中不包含 data 属性")

    # 重置文件指针以便后续使用
    await file.seek(0)
    # 调用 InternVL3-latest 接口查看图片内容
    llm_result = await service.call_llm(file,auth.user.id)
    # 幂等性校验
    check_idempotency_result = await service.check_idempotency(file_content,auth.user.id)
    if getattr(check_idempotency_result, 'data', None) and isinstance(check_result.data,dict) and check_result.data.get('code') == 200:
        # 重置文件指针以便后续使用
        await file.seek(0)

        # 上传图片到阿里云 OSS
        filepath = ALIYUN_OSS_INTELIGENT_PATH
        result = await AliyunOSS(BucketConf(**ALIYUN_OSS)).upload_image(filepath, file)
        print(f"上传结果：{result}")

        data = schemas.DrawingImagesRecord(
            filename=file.filename,
            image_url=result,
            create_user_id=auth.user.id,
            file_size=100,
            image_type="jpg"
        )
    else:
        print("返回结果的 data 属性下不包含 data 字段")

    return SuccessResponse(await crud.DrawingImagesRecordDal(auth.db).create_data(data=data))


@app.get("/drawing/images/record", summary="获取AI智慧上传图片列表", tags=["AI智慧上传图片"])
async def get_drawing_images_record_list(p: params.DrawingImagesRecordParams = Depends(), auth: Auth = Depends(AllUserAuth())):
    datas, count = await crud.DrawingImagesRecordDal(auth.db).get_datas(**p.dict(), v_return_count=True)
    return SuccessResponse(datas, count=count)


@app.post("/drawing/images/record", summary="创建AI智慧上传图片", tags=["AI智慧上传图片"])
async def create_drawing_images_record(data: schemas.DrawingImagesRecord, auth: Auth = Depends(AllUserAuth())):
    return SuccessResponse(await crud.DrawingImagesRecordDal(auth.db).create_data(data=data))


@app.delete("/drawing/images/record", summary="删除AI智慧上传图片", description="硬删除", tags=["AI智慧上传图片"])
async def delete_drawing_images_record_list(ids: IdList = Depends(), auth: Auth = Depends(AllUserAuth())):
    await crud.DrawingImagesRecordDal(auth.db).delete_datas(ids=ids.ids, v_soft=False)
    return SuccessResponse("删除成功")


@app.put("/drawing/images/record/{data_id}", summary="更新AI智慧上传图片", tags=["AI智慧上传图片"])
async def put_drawing_images_record(data_id: int, data: schemas.DrawingImagesRecord, auth: Auth = Depends(AllUserAuth())):
    return SuccessResponse(await crud.DrawingImagesRecordDal(auth.db).put_data(data_id, data))


@app.get("/drawing/images/record/{data_id}", summary="获取AI智慧上传图片信息", tags=["AI智慧上传图片"])
async def get_drawing_images_record(data_id: int, db: AsyncSession = Depends(db_getter)):
    schema = schemas.DrawingImagesRecordSimpleOut
    return SuccessResponse(await crud.DrawingImagesRecordDal(db).get_data(data_id, v_schema=schema))




###########################################################
#    AI智慧上传图片
###########################################################
@app.get("/drawing/images/record", summary="获取AI智慧上传图片列表", tags=["AI智慧上传图片"])
async def get_drawing_images_record_list(p: params.DrawingImagesRecordParams = Depends(), auth: Auth = Depends(AllUserAuth())):
    datas, count = await crud.DrawingImagesRecordDal(auth.db).get_datas(**p.dict(), v_return_count=True)
    return SuccessResponse(datas, count=count)


@app.post("/drawing/images/record", summary="创建AI智慧上传图片", tags=["AI智慧上传图片"])
async def create_drawing_images_record(data: schemas.DrawingImagesRecord, auth: Auth = Depends(AllUserAuth())):
    return SuccessResponse(await crud.DrawingImagesRecordDal(auth.db).create_data(data=data))


@app.delete("/drawing/images/record", summary="删除AI智慧上传图片", description="硬删除", tags=["AI智慧上传图片"])
async def delete_drawing_images_record_list(ids: IdList = Depends(), auth: Auth = Depends(AllUserAuth())):
    await crud.DrawingImagesRecordDal(auth.db).delete_datas(ids=ids.ids, v_soft=False)
    return SuccessResponse("删除成功")


@app.put("/drawing/images/record/{data_id}", summary="更新AI智慧上传图片", tags=["AI智慧上传图片"])
async def put_drawing_images_record(data_id: int, data: schemas.DrawingImagesRecord, auth: Auth = Depends(AllUserAuth())):
    return SuccessResponse(await crud.DrawingImagesRecordDal(auth.db).put_data(data_id, data))


@app.get("/drawing/images/record/{data_id}", summary="获取AI智慧上传图片信息", tags=["AI智慧上传图片"])
async def get_drawing_images_record(data_id: int, db: AsyncSession = Depends(db_getter)):
    schema = schemas.DrawingImagesRecordSimpleOut
    return SuccessResponse(await crud.DrawingImagesRecordDal(db).get_data(data_id, v_schema=schema))

