import os
import asyncio
import aiofiles
import json
import io

from fastapi import HTTPException, UploadFile, File
from PIL import Image

from ocr.angle import closed_angle_of_result
from ocr.ocr import ocr_image_from_bytesio
from ocr.image import rotate_image, draw_red_dot_and_label_with_image
from utils.image import bytesio_with_binary_data, image_with_bytesio, bytesio_with_image


RESULT_IMAGE_DIRECTORY = "/paddle/images/ocr/result"
ORIGINAL_IMAGE_DIRECTORY = "/paddle/images/ocr/original"
OCR_JSON_SAVE_DIRECTORY = "/paddle/images/ocr/json"

# class OCR:

#     def __init__(self, file_name) -> None:
#         self.file_name = file_name
#         self.clockwise_value = 0
#         self.bytesio = None
#         self.origin_results = []
#         self.rotated_result = []
#         pass


# file_name: 原始文件名
# angle_value: 旋转的角度，如果为-1则为该图片未识别成功，未旋转
# clockwise: 1为顺时针旋转，-1为逆时针旋转
# original_result: 原图ocr识别结果
# rotated_result: 原图旋转anglevalue角度后重新ocr识别的结果
def final_result(code: int, file_name: str, angle_value: float, clock_wise: bool, original_result: list, rotated_result: list) -> dict:
    return {
        'status': code,
        'result': {
            'filename': file_name,
            'anglevalue': angle_value,
            'clockwise': clock_wise,
            'original': original_result,
            'rotated': rotated_result
        }
    }


# 计算逆时针旋转的角度
def count_the_real_angle_of_anticlockwise(angle_value: float) -> float:
    return angle_value if angle_value >= 0 else angle_value + 360


# 异步保存图片到指定路径
async def save_image(file_path: str, image: Image) -> None:
    async with open(file_path, 'wb') as f:
        image.save(f, format='PNG')


# 保存原图
def save_original_image(file_name:str, image:Image) -> None:
    full_path = os.path.join(ORIGINAL_IMAGE_DIRECTORY, file_name)
    save_image(full_path, image)


# 异步保存json文件
async def save_json_file(file_name: str, result: list) -> None:
    json_file = json.load(result)
    json_name = os.path.splitext(file_name)[0] + '.json'
    full_path = os.path.join(OCR_JSON_SAVE_DIRECTORY, json_name)
    async with open(full_path, 'wb', encoding='utf-8') as f:
        json.dump(json_file, f, ensure_ascii=False, indent=4)


# 绘制描点后保存图片
async def save_result_image(file_name: str, image: Image, result: list, angle_value=None) -> None:
    # async def inner():
    #     image_aft_draw = await draw_red_dot_and_label_with_image(image, result, angle_value)
    #     full_path = os.path.join(RESULT_IMAGE_DIRECTORY, file_name)
    #     save_image(full_path, image_aft_draw)
    # asyncio.run(inner())
    image_aft_draw = await draw_red_dot_and_label_with_image(image, result, angle_value)
    full_path = os.path.join(RESULT_IMAGE_DIRECTORY, file_name)
    save_image(full_path, image_aft_draw)


# 获取图片ocr结果数据
# def result_with_binary_data(bytesio: bytes, file_name: str) -> dict:
def result_with_binary_data(bytesio: io.BytesIO, file_name: str) -> dict:
    # 初始化BytesIO字节串
    
    # 保存原图
    save_original_image(file_name, image_with_bytesio(bytesio))

    # 第一次ocr，开启文字方向识别器
    origin_result = ocr_image_from_bytesio(bytesio, True, 'ch')
    # 识别结果为空，直接返回
    if len(origin_result) == 0:
        return final_result(200, file_name, -1, False, [], [])
    # 计算最佳旋转角度
    angle_value = closed_angle_of_result(origin_result)
    # 异步保存识别标注后的图片
    # asyncio.run(save_result_image(file_name, image_with_bytesio(bytesio), origin_result, angle_value))
    # 保存识别标注后的图片
    save_result_image(file_name, image_with_bytesio(bytesio), origin_result, angle_value)
    
    # 角度 < 1 直接返回，不进行旋转
    if abs(angle_value) < 1:
        return final_result(200, file_name, angle_value, False, origin_result, [])
    # 计算实际旋转角度
    anticlosewise = count_the_real_angle_of_anticlockwise(angle_value)
    # 旋转图片
    rotated_image = rotate_image(bytesio, anticlosewise)
    # 获取旋转后图片的BytesIO字节串
    rotated_bytesio = bytesio_with_image(rotated_image)
    # 第二次ocr，关闭文字方向识别器
    rotated_result = ocr_image_from_bytesio(rotated_bytesio, False, 'ch')

    # 旋转后的图片名称
    rotated_file_name = os.path.splitext(file_name)[0] + '_rotated.png'
    # 异步保存第二次识别标注后的图片
    # asyncio.run(save_result_image(rotated_file_name, rotated_image, rotated_result))
    # 保存第二次识别标注后的图片
    save_result_image(rotated_file_name, rotated_image, rotated_result)

    final = final_result(200, file_name, anticlosewise, False, origin_result, rotated_result)
    # 保存最终json文件
    save_json_file(file_name, final)

    return final


# 获取图片识别结果
async def response_data_from_body(file: UploadFile = File(...)) -> dict:
    if not file.content_type:
        raise HTTPException(status_code=400, detail="未提供文件")

	# 为文件生成唯一的文件名
    file_name = f"{hash(file.content_type)}_{file.filename}"
	# 读取文件的二进制数据
    binary_data = await file.read()
    # bytesio = io.BytesIO(binary_data)
    bytesio = bytesio_with_binary_data(binary_data)
	# 将二进制数据保存到内存
    return result_with_binary_data(bytesio, file_name)
	

