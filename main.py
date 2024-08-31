from fastapi import FastAPI, File, UploadFile, HTTPException, Body
import os
import io
import subprocess
import re
from utils.ocrresponse import response_data_with_binary_data
from app.ocr import response_data_from_body


app = FastAPI()

# 指定文件保存的目录
DETECTION_SAVE_DIRECTORY = "/paddle/images/detection"
OCR_SAVE_DIRECTORY = "/paddle/images/ocr"

# 指定Detection项目目录
DETECTION_PATH = "/paddle/PaddleDetection/"

# 确保保存目录存在
os.makedirs(DETECTION_SAVE_DIRECTORY, exist_ok=True)
os.makedirs(OCR_SAVE_DIRECTORY, exist_ok=True)

# 用于存储内存中的文件对象
memory_files = {}

def get_image():
	if memory_files == {}:
		return None
	else:
		return memory_files

@app.get("/")
def read_root():
	return {"Hello": "world"}





# 上传图片，保存到指定目录并保存到内存
@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
	# 确认文件是图片
	if file.content_type not in ['image/jpeg', 'image/png', 'image/gif']:
		raise HTTPException(status_code=400, detail="不支持的文件类型")

	# 为文件生成唯一的文件名
	filename = f"{hash(file.content_type)}_{file.filename}"
	file_path = os.path.join(DETECTION_SAVE_DIRECTORY, filename)

	# 将上传的文件内容读取到内存
	file_content = await file.read()
	memory_file = io.BytesIO(file_content)

	# 保存到内存中，使用文件名作为键
	memory_files[filename] = memory_file

	# 将上传的文件保存到指定目录
	with open(file_path, "wb") as f:
		f.write(file_content)

	img_file = "--image_file=" + file_path
	infer_file = DETECTION_PATH + "deploy/python/infer.py"
	# "--model_dir=./output_inference/picodet_lcnet_x2_5_640_mainbody"
	model_dir = "--model_dir=" + DETECTION_PATH + "output_inference/picodet_lcnet_x2_5_640_mainbody" 
	command = [
		"python", 
		infer_file,
		model_dir,
		img_file
	]

	# 使用subprocess.run执行命令
	result = subprocess.run(command, capture_output=True, text=True)
	
	# 获取命令的标准输出和标准错误
	stdout = result.stdout
	stderr = result.stderr

	# 打印输出和错误（可选）
	print("STDOUT:", stdout)
	print("STDERR:", stderr)

	pattern = r"class_id:(\d+), confidence:([0-9.]+), left_top:\[([0-9.]+),([0-9.]+)\],right_bottom:\[([0-9.]+),([0-9.]+)\]"
	# 使用正则表达式查找所有匹配项
	matches = re.findall(pattern, stdout)
	# 将匹配项组装成字典列表
	results = [
		{
			"class_id": int(class_id),
			"confidence": float(confidence),
			"bounding_box": {
				"left_top": [float(x), float(y)],
				"right_bottom": [float(w), float(h)]
			}
		}
		for class_id, confidence, x, y, w, h in matches
	]

	# 检查命令是否成功执行
	if result.returncode == 0:
		return {"status": "success", "filename": filename, "logs": results}
	else:
		return {"status": "error", "error": stderr}


@app.post("/image-detection/")
async def upload_binary_data(file: UploadFile = File(...)):
	# 检查文件是否为空
	if not file.content_type:
		raise HTTPException(status_code=400, detail="未提供文件")

	# 为文件生成唯一的文件名
	filename = f"{hash(file.content_type)}_{file.filename}"
	print(f'filename = {filename}')
	print(f'content_type = {file.content_type}')

	file_path = os.path.join(DETECTION_SAVE_DIRECTORY, filename)
	print(f'file_path = {file_path}')
	# 读取文件的二进制数据
	binary_data = await file.read()

	#print(f'binary_data = {binary_data}')

	memory_files[filename] = binary_data

	# 将上传的文件保存到指定目录
	with open(file_path, "wb") as f:
		f.write(binary_data)

	img_file = "--image_file=" + file_path
	infer_file = DETECTION_PATH + "deploy/python/infer.py"
	# "--model_dir=./output_inference/picodet_lcnet_x2_5_640_mainbody"
	model_dir = "--model_dir=" + DETECTION_PATH + "output_inference/picodet_lcnet_x2_5_640_mainbody" 
	command = [
		"python", 
		infer_file,
		model_dir,
		img_file
	]

	# 使用subprocess.run执行命令
	result = subprocess.run(command, capture_output=True, text=True)

	# 获取命令的标准输出和标准错误
	stdout = result.stdout
	stderr = result.stderr

	# 打印输出和错误（可选）
	print("STDOUT:", stdout)
	print("STDERR:", stderr)

	pattern = r"class_id:(\d+), confidence:([0-9.]+), left_top:\[([0-9.]+),([0-9.]+)\],right_bottom:\[([0-9.]+),([0-9.]+)\]"
	# 使用正则表达式查找所有匹配项
	matches = re.findall(pattern, stdout)
	# 将匹配项组装成字典列表
	results = [
		{
			"class_id": int(class_id),
			"confidence": float(confidence),
			"bounding_box": {
			"left_top": [float(x), float(y)],
			"right_bottom": [float(w), float(h)]
			}
		}
		for class_id, confidence, x, y, w, h in matches
	]

	# 检查命令是否成功执行
	if result.returncode == 0:
		return {
			"status": 200,
			"result": {
				"filename": filename,
				"detections": results
			}
		}
	else:
		return {
			"status": 0,
			"result": {
				"filename": filename,
				"error": stderr
			}
		}



@app.post("/image-ocr/")
async def ocr_binary_data(file: UploadFile = File(...)):
	
	return response_data_from_body(file)
	
	##################################################
	# 以下为另一个实现逻辑
	##################################################

	# 检查文件是否为空
	# if not file.content_type:
	# 	raise HTTPException(status_code=400, detail="未提供文件")
	
	# # 为文件生成唯一的文件名
	# filename = f"{hash(file.content_type)}_{file.filename}"
	# # 读取文件的二进制数据
	# Coroutine[Any, Any, bytes]
	# binary_data = await file.read()
	# # 将二进制数据保存到内存
	# memory_files[filename] = binary_data
	# final_result = response_data_with_binary_data(binary_data, filename)
	# return final_result

	##################################################
	# 以下为另一个实现逻辑
	##################################################
	
	# # 为文件生成唯一的文件名
	# filename = f"{hash(file.content_type)}_{file.filename}"
	# print(f'filename = {filename}')
	# print(f'content_type = {file.content_type}')
	
	# file_path = os.path.join(OCR_SAVE_DIRECTORY, filename)
	# print(f'file_path = {file_path}')
	# # 读取文件的二进制数据
	# binary_data = await file.read()

	# #print(f'binary_data = {binary_data}')

	# memory_files[filename] = binary_data

	# # 将上传的文件保存到指定目录
	# # with open(file_path, "wb") as f:
	# 	# f.write(binary_data)

	# # 识别图片
	# result = ocr_image_from_bytes(binary_data, True, "ch")
	# if len(result) == 0:
	# 	# 将图片保存
	# 	with open(file_path, "wb") as f:
	# 		f.write(binary_data)
	# 	# 返回结果
	# 	final_result = {
	# 		"status": "200",
	# 		"result": {
	# 			"filename": filename,
	# 			"anglevalue": 0,
	# 			"clockwise": 1,
	# 			"initial": result,
	# 			"rotated": []
	# 		}
	# 	}
	# 	return final_result
	# # 在图片上标注识别出的坐标信息
	# original_img = draw_red_dot_and_label_with_binary_data(io.BytesIO(binary_data) , result)
	# # 将图片保存到指定目录
	# original_img.save(file_path, format='PNG')
    
	# # 距离其他偏转角度最近的角度
	# anglevalue = closed_angle_of_result(result)

	# # 角度 < 1 直接返回，不进行旋转
	# if abs(anglevalue) < 1:
	# 	final_result = {
	# 		"status": "200",
	# 		"result": {
	# 			"filename": filename,
	# 			"anglevalue": anglevalue,
	# 			"clockwise": 1,
	# 			"initial": result,
	# 			"rotated": []
	# 		}
	# 	}		
	# 	return final_result

	# # 图片旋转方法rotate_image_with_binary_data的参数vv为负值，将图片顺时针旋转；vv为正值，将图片逆时针旋转
	# # 如果anglevalue > 0，需要逆时针旋转，如果anglevalue < 0，需要顺时针旋转
	# vv = anglevalue
	# img = rotate_image_with_binary_data(io.BytesIO(binary_data), vv)
	# if anglevalue < 0:
	# 	rotated = 'clockwise'
	# 	clockwise = 1
	# else:
	# 	rotated = 'anticlockwise'
	# 	clockwise = 0
	# rotated_file_name = os.path.splitext(filename)[0] + '_' + rotated + '.png'
	# rotated_file_path = os.path.join(OCR_SAVE_DIRECTORY, rotated_file_name)
	# print(f'rotated_file_path = {rotated_file_path}')
	# # img.save(rotated_file_path, format='PNG')
	# byte_io = io.BytesIO()
	# img.save(byte_io, format='PNG')
	# image_bytes = byte_io.getvalue()
	# rotated_result = ocr_image_from_bytes(image_bytes, False, 'ch')
	# rotated_image = draw_red_dot_and_label_with_image(img, rotated_result)
	# rotated_image.save(rotated_file_path, format='PNG')
	# final_result = {
	# 	'status': 200,
	# 	'result': {
	# 		'filename': filename,
	# 		'anglevalue': anglevalue,
	# 		'clockwise': clockwise,
	# 		'initial':result,
	# 		'rotated': rotated_result
	# 	}
	# }

	# # 虽然此处直接返回了，还可以向后延伸
	# # rotated_result是旋转后再次识别的结果，本次识别未开启文字方向识别器。
	# # 如果识别效果很差，则将其旋转180°后应该方向正确
	# # 此时关闭文字方向识别器再次识别文字，识别结果与第一次相近或者更好
	# return final_result


# 设置Uvicorn服务器的运行
if __name__ == "__main__":
	import uvicorn
	uvicorn.run(app, host="0.0.0.0", port=8000)