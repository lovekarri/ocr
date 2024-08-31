import io

from PIL import Image, ImageDraw, ImageFont


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
    