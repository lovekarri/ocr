from PIL import Image, ImageDraw, ImageFont


# 将图片旋转指定角度后生成新图片
# img: 待旋转的图片对象
# angle: 旋转的角度 - 顺时针为正，负值时为逆时针旋转，正值时为顺时针旋转
def rotate_image(img: Image, angle: float) -> Image:
  
  # 当expand=True时，旋转后的图像会扩展以适应整个旋转后的图像区域，这意味着图像的尺寸会根据旋转角度进行调整，以确保旋转后的图像不会被裁剪。
  # 当expand=False（默认值）时，旋转后的图像尺寸与原始图像相同，可能会导致部分图像被裁剪。
  rotated_img = img.rotate(angle, expand=True)
  return rotated_img


# 在图片上把红点画出来并将坐标位置写在旁边
# img: 图片
# result: ocr识别出的文字信息
async def draw_red_dot_and_label_with_image(img: Image, result: list, anglevalue=None) -> Image:
    draw = ImageDraw.Draw(img)
    # 加载字体
    font = ImageFont.load_default()
    # 如果角度不为空，将角度绘制在图片左上角
    if anglevalue != None:
        angle_font = ImageFont.truetype('Arial.ttf', size=30)
        textvalue = f'{anglevalue}'
        textvalue_width, textvalue_height = draw.textsize(textvalue, angle_font)
        draw.text((20, 20 - textvalue_height // 2), textvalue, font=angle_font, fill='red')

    # 将每个点的信息绘制出来
    for item in result:
        point_list = item.get('box')
        for point in point_list:
            x = point[0]
            y = point[1]
            # 画红点
            dot_size = 5
            draw.ellipse((x - dot_size, y - dot_size, x + dot_size, y + dot_size), fill='red')
            # 绘制坐标文本
            text = f'({x}, {y})'
            text_width, text_height = draw.textsize(text, font=font)
            draw.text((x + dot_size + 5, y - text_height // 2), text, font=font, fill='black')

    return img


# 在图片上把红点画出来并将坐标位置写在旁边
# binary_data: 图片的二进制字节串
# result: ocr识别出的文字信息
def draw_red_dot_and_label_with_binary_data(binary_data, result):
    img = Image.open(binary_data) 
    img2 = draw_red_dot_and_label_with_image(img, result)
    return img2