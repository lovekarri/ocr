from fastapi import FastAPI, File, UploadFile, HTTPException, Body
import os
import io
import subprocess
import re
from utils.ocrresponse import response_data_with_binary_data


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
    # 检查文件是否为空
    if not file.content_type:
        raise HTTPException(status_code=400, detail="未提供文件")

    # 为文件生成唯一的文件名
    filename = f"{hash(file.content_type)}_{file.filename}"
    # 读取文件的二进制数据
    binary_data = await file.read()
    # 将二进制数据保存到内存
    memory_files[filename] = binary_data
    final_result = response_data_with_binary_data(binary_data, filename)
    return final_result




# 设置Uvicorn服务器的运行
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)