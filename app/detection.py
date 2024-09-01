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

# 用于存储内存中的文件对象
# memory_files = {}

# def get_image():
# 	if memory_files == {}:
# 		return None
# 	else:
# 		return memory_files



# def result_with_bytesio(bytesio: io.BytesIO, file_name: str) -> dict:



# 获取图片识别结果
# async def response_data_from_body(file: UploadFile = File(...)) -> dict:

#     memory_files[filename] = binary_data
    
#     return {}