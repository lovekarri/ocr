import os
import io
import asyncio

from fastapi import HTTPException, UploadFile, File



# 指定文件保存的目录
DETECTION_SAVE_DIRECTORY = "/paddle/images/detection"

# 指定Detection项目目录
DETECTION_PATH = "/paddle/PaddleDetection/"

# 确保保存目录存在
os.makedirs(DETECTION_SAVE_DIRECTORY, exist_ok=True)



def result_with_bytesio(bytesio: io.BytesIO, file_name: str) -> dict:



# 获取图片识别结果
async def response_data_from_body(file: UploadFile = File(...)) -> dict:
    
    return {}