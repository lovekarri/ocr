from paddleocr import PaddleOCR
import io
from PIL import Image
import numpy as np

def json_with_result(result):
	result_list = []
	# print(f"result = {result}")
	if len(result) > 0:
		for item in result:
			box = item[0]
			text = item[1][0]
			rate = item[1][1]
			# print(f'box = {box}, box len = {len(box)}')
			# angle = angle_of_longer_side_rectangle(box)
			result_list.append({
				"box":box,
				"text": text,
				"rate": rate,
				# "angle": angle
			})
	
	return result_list


# ocr识别图片上的文字，输入为图片二进制字节流
def ocr_image_from_bytesio(image_bytes, use_angle_cls=True, lang="ch"):
	temp_image = Image.open(image_bytes)
	if temp_image.mode == 'RGBA':
		temp_image = temp_image.convert('RGB')

	ocr = PaddleOCR(use_angle_cls=use_angle_cls, lang=lang)
	result = ocr.ocr(np.array(temp_image), cls=use_angle_cls)
	return json_with_result(result=result)
