import os
import io
import asyncio
import re
import subprocess

from fastapi import HTTPException, UploadFile, File



# 指定文件保存的目录
DETECTION_SAVE_DIRECTORY = "/paddle/images/detection"

# 指定Detection项目目录
DETECTION_PATH = "/paddle/PaddleDetection/"

# 确保保存目录存在
os.makedirs(DETECTION_SAVE_DIRECTORY, exist_ok=True)


# 将文件保存到指定目录
def save_image(file_path: str, binary_data: bytes) -> None:
    with open(file_path, 'wb') as f:
        f.write(binary_data)


def detection(file_path: str):
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
    return result


def results_with_re(result) -> list:
    pattern = r"class_id:(\d+), confidence:([0-9.]+), left_top:\[([0-9.]+),([0-9.]+)\],right_bottom:\[([0-9.]+),([0-9.]+)\]"
    # 使用正则表达式查找所有匹配项
    matches = re.findall(pattern, result)

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
    return results


def result_with_binary_data(binary_data: bytes, file_name: str) -> dict:
    file_path = os.path.join(DETECTION_SAVE_DIRECTORY, file_name)
    print(f'file_path = {file_path}')

    # 将上传的文件保存到指定目录
    save_image(file_path, binary_data)

    result = detection(file_path)

    # 获取命令的标准输出和标准错误
    stdout = result.stdout
    stderr = result.stderr

    # 打印输出和错误（可选）
    print("STDOUT:", stdout)
    print("STDERR:", stderr)

    results = results_with_re(result.stdout)

    # 检查命令是否成功执行
    if result.returncode == 0:
        return {
            "status": 200,
            "result": {
                "filename": file_name,
                "detections": results
            }
        }
    else:
        return {
            "status": 0,
            "result": {
                "filename": file_name,
                "error": stderr
            }
        }


# 获取图片识别结果
async def response_data_from_body(file: UploadFile = File(...)) -> dict:
    
    return {}