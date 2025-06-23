#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/06/22 16:52
# @File           : views.py
# @IDE            : PyCharm
# @desc           : 路由，视图文件
import mimetypes
from io import BytesIO

from PIL.Image import Image
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, UploadFile, HTTPException
from . import models, schemas, crud, params
from core.dependencies import IdList
from apps.vadmin.auth.utils.current import AllUserAuth
from utils.response import SuccessResponse
from apps.vadmin.auth.utils.validation.auth import Auth
from core.database import db_getter
from apps.vadmin.auth.utils.current import FullAdminAuth
from application.settings import ALIYUN_OSS, ALIYUN_OSS_INTELIGENT_PATH
from utils.file.aliyun_oss import AliyunOSS, BucketConf
from service.viewsCheckService import ViewsCheckService

app = APIRouter()


###########################################################
#    AI智慧上传图片
###########################################################
@app.post("/drawing/images/uploadImg", summary="上传图片", tags=["AI智慧上传图片"])
async def upload_images(file: UploadFile, auth: Auth = Depends(FullAdminAuth())):
    # 图片校验

    ## 获取文件名称
    ViewsCheckService.check_image_validity(UploadFile)
    # 重置文件指针以便后续使用
    await file.seek(0)

    # 幂等性校验
    service = ViewsCheckService()


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

