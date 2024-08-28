from paddleocr import PaddleOCR
import json
import base64
import io
import os
from PIL import Image
import numpy as np
from .util import angle_of_longer_side_rectangle


def list_with_result(result):
    result_list = []
    print(f"result = {result}")
    if len(result) > 0:
        for item in result:
            box = item[0]
            text = item[1][0]
            rate = item[1][1]
            # print(f'box = {box}, box len = {len(box)}')
            angle = angle_of_longer_side_rectangle(box)
            result_list.append({
                "box":box,
                "text": text,
                "rate": rate,
                "angle": angle
            })
            # print(f"box: {box}, text: {text}, rate: {rate}, angle: {angle}")

    # json_result = json.dumps(result_list)
    # print(f"json_result = {json_result}")
        
    return result_list


IMAGE_PATH = '/paddle/ocr/res/'


def path_with_image_name(image_name):
    return os.path.join(IMAGE_PATH, image_name)


def result_from_ocr_with_path(image_path, use_angle_cls=True, lang="ch"):
    '''
    ocr识别图片上的文字，输入未图片存储路径
    >>> len(result_from_ocr_with_path(path_with_image_name('blood_pressure_355.jpg'), True, lang)) > 0
    True    
    '''
    ocr = PaddleOCR(use_angle_cls=use_angle_cls, lang=lang)
    return ocr.ocr(image_path)    


# ocr识别图片上的文字，输入未图片存储路径
# use_angle_cls: True为开启文本方向识别器，默认开启
# lang: 识别语言，默认中文
def ocr_image_with_path(image_path, use_angle_cls=True, lang="ch"):
    result = result_from_ocr_with_path(image_path, use_angle_cls, lang)
    return list_with_result(result)


def load_img_with_name(image_name):
    image_path = path_with_image_name(image_name)
    with open(image_path, 'rb') as f:
        return f.read()
    

def result_from_ocr_with_bytes(image_bytes, use_angle_cls=True, lang='ch'):
    '''
    ocr识别图片上的文字，输入为图片二进制字节流    
    >>> len(result_from_ocr_with_bytes(load_img_with_name('blood_pressure_355.jpg'), use_angle_cls=True, lang="ch")) > 0
    True
    '''

    temp_image = Image.open(io.BytesIO(image_bytes))
    if temp_image.mode == 'RGBA':
        temp_image = temp_image.convert('RGB')
    # temp_image = image_bytes

    ocr = PaddleOCR(use_angle_cls=use_angle_cls, lang=lang)
    return ocr.ocr(np.array(temp_image), use_angle_cls, lang)    


# ocr识别图片上的文字，输入为图片二进制字节流
def ocr_image_from_bytes(image_bytes, use_angle_cls=True, lang="ch"):

    result = result_from_ocr_with_bytes(image_bytes, use_angle_cls, lang)
    return list_with_result(result=result)


if __name__ == '__main__':
    import doctest
    print(doctest.testmod(verbose=False, report=False))