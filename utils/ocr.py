from paddleocr import PaddleOCR
import json
import base64
import io
from PIL import Image
import numpy as np
# from utils.util import angle_of_longer_side_rectangle
from util import angle_of_longer_side_rectangle


def json_with_result(result):
	result_list = []
	# print(f"result = {result}")
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
	# return json_result	
	return result_list




# ocr识别图片上的文字，输入未图片存储路径
# use_angle_cls: True为开启文本方向识别器，默认开启
# lang: 识别语言，默认中文
def ocr_image_with_path(image_path, use_angle_cls=True, lang="ch"):
	ocr = PaddleOCR(use_angle_cls=use_angle_cls, lang=lang)
	result = ocr.ocr(image_path)
	return json_with_result(result)


# ocr识别图片上的文字，输入为图片二进制字节流
def ocr_image_from_bytes(image_bytes, use_angle_cls=True, lang="ch"):
	# img_data = base64.b16encode(image_bytes).decode('utf-8')
	# img_base64 = f"data:image/jpeg;base64,{img_data}"
	temp_image = Image.open(io.BytesIO(image_bytes))
	if temp_image.mode == 'RGBA':
		temp_image = temp_image.convert('RGB')
	# temp_image = image_bytes

	ocr = PaddleOCR(use_angle_cls=use_angle_cls, lang=lang)
	result = ocr.ocr(np.array(temp_image), cls=use_angle_cls)
	# result = ocr.ocr(io.BytesIO(image_bytes),True, 'ch')
	return json_with_result(result=result)


