import io
import cv2
import numpy as np
import os

from PIL import Image, ImageDraw, ImageFont


def is_image(file_path):
    extension = os.path.splitext(file_path)[1].lower()
    return extension in ['.jpg', '.png', '.jpeg']


# 从二进制字节流生成BytesIO字节串
def bytesio_with_binary_data(binary_data: bytes) -> io.BytesIO:
    return io.BytesIO(binary_data)


# 从BytesIO字节串生成Image对象
def image_with_bytesio(bytesio: io.BytesIO) -> Image:
    return Image.open(bytesio)


# 从Image对象生成BytesIO字节串
def bytesio_with_image(image: Image) -> io.BytesIO:
    byte_io = io.BytesIO()
    image.save(byte_io, format='PNG')
    return byte_io


# pil读出的Image对象转为cv2的nd.ndarray数组
def pil_image_to_cv2_image(image: Image) -> np.ndarray:
    img = np.array(image)

    # 如果图片是RGBA格式，将其转换为RGB格式
    if len(img.shape) == 3 and img.shape[2] == 4:
        img = img[:, :, :3]

    # 如果图片是彩色图像，且为RGB格式，转换颜色通道顺序为BGR
    if len(img.shape) == 3 and img.shape[2] == 3:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    return img
    

# 从Image对象生成灰度图像
def image_to_gray_image(image: Image) -> np.ndarray:
    img = pil_image_to_cv2_image(image)

    # 将BGR图片转换为灰度图片
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return gray_image
    

# 从灰度图像生成边缘检测后的二值图像
def canny_edges_of_image(image: np.ndarray, low_value=50, high_value=150, apertureSize=3) -> np.ndarray:
    edges = cv2.Canny(image, low_value, high_value, apertureSize)
    return edges