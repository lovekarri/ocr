import math
from PIL import Image

# 计算两个点之间连线与水平线的夹角（该连线顺时针旋转后与水平方向平行的角度）
# x1: 第一个点的x坐标
# y1: 第一个点的y坐标
# x2: 第二个点的x坐标
# y2: 第二个点的y坐标
def angle_between_two_points(x1, y1, x2, y2):
    print(f'(x1, y1) = ({x1}, {y1}), (x2,y2) = ({x2}, {y2})')
    print(f"y2-y1 = {y2 - y1}, x2-x1 = {x2 - x1}")
    if x2 == x1:
        slope = None
    else:
        slope = (y1 - y2) / (x2 - x1)

    # 计算倾角（角度制）
    if slope is None:
        angle = 90
    else:
        angle = math.degrees(math.atan(slope))

    # 由于坐标零点在图片左上角，angle与坐标零点在图片左下角正相反
    # 可以考虑将坐标系翻转到左下角，angle直接取反
    # angle  = 0 - angle

    if angle < 0:
        angle += 180
  
    return angle


# 求识别结果中偏转角度距离其他角度距离最近的那个
def closed_angle_of_result(result):
    angles = []
    for item in result:
        angles.append(item.get('angle'))

    n = len(angles)
    if n < 2:
        return angles[0] if n > 0 else None
    min_distance = float('inf')
    closest_value = None
    for i in range(n):
        current_value = angles[i]
        total_distance = 0
        for j in range(n):
            if i!= j:
                total_distance += abs(current_value - angles[j])
        if total_distance < min_distance:
            min_distance = total_distance
            closest_value = current_value
    return closest_value
    
    # try:
    #     n = len(angles)
    #     if n < 2:
    #         return angles[0] if n > 0 else None
        
    #     # 计算差值矩阵
    #     diff_matrix = [[0] * n for _ in range[0]]
    #     for i in range(n):
    #         for j in range(n):
    #             diff_matrix[i][j] = abs(angles[i] - angles[j])
        
    #     min_distance = float('inf')
    #     closest_value = None
    #     for i in range(n):
    #         total_distance = sum(diff_matrix[i])
    #         if total_distance < min_distance:
    #             min_distance = total_distance
    #             closest_value = angles[i]

    #     return closest_value            

    # except TypeError as e:
    #     print(f'数据类型错误：{e}')    
    #     return None


# 计算已知矩形4个顶点坐标时其长边与水平线夹角
# rectangle_points: 数组，限制长度为4个元素，每个元素为矩形的1个顶点坐标 
def angle_of_longer_side_rectangle(rectangle_points):
    print(f'rectangle_points = {rectangle_points}, len = {len(rectangle_points)}')
    assert isinstance(rectangle_points, list), "函数入参应该是数组"
    assert len(rectangle_points) == 4, "函数入参数组长度应为4"
    for point in rectangle_points:
       assert isinstance(point, list), "每个元素都应该是数组"
       assert len(point) == 2, "每个元素长度都应该为2"
       assert isinstance(point[0], float), "x值应该是浮点数"
       assert isinstance(point[1], float), "y值应该是浮点数"

    
    # 假设传入的四个点按顺序为 A、B、C、D
    x1, y1 = rectangle_points[0]
    x2, y2 = rectangle_points[1]
    x3, y3 = rectangle_points[2]
    x4, y4 = rectangle_points[3]

    # 计算边长
    side1_length = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
    side2_length = ((x3 - x2)**2 + (y3 - y2)**2)**0.5
    side3_length = ((x4 - x3)**2 + (y4 - y3)**2)**0.5
    side4_length = ((x1 - x4)**2 + (y1 - y4)**2)**0.5

    # 判断长边
    if side1_length > side2_length:
        longer_side_points = (x1, y1), (x2, y2)
    else:
        longer_side_points = (x2, y2), (x3, y3)

    if side3_length > side4_length:
        if side3_length > max(side1_length, side2_length):
            longer_side_points = (x3, y3), (x4, y4)
    else:
        if side4_length > max(side1_length, side2_length):
            longer_side_points = (x4, y4), (x1, y1)

    x1, y1 = longer_side_points[0]
    x2, y2 = longer_side_points[1]

    if x1 < x2:
        return angle_between_two_points(x1, y1, x2, y2)
    else:
        return angle_between_two_points(x2, y2, x1, y1)


# 将图片旋转指定角度后生成新图片
# image_path: 图片的保存路径
# angle: 旋转的角度 - 顺时针为正，负值时为逆时针旋转，正值时为顺时针旋转
def rotate_image(image_path, angle):
  img = Image.open(image_path)
  # 当expand=True时，旋转后的图像会扩展以适应整个旋转后的图像区域，这意味着图像的尺寸会根据旋转角度进行调整，以确保旋转后的图像不会被裁剪。
  # 当expand=False（默认值）时，旋转后的图像尺寸与原始图像相同，可能会导致部分图像被裁剪。
  rotated_img = img.rotate(angle, expand=True)
  return rotated_img


# 将图片旋转指定角度后生成新图片
# binary_data: 图片的保存路径
# angle: 旋转的角度 - 顺时针为正，负值时为逆时针旋转，正值时为顺时针旋转
def rotate_image_with_binary_data(binary_data, angle):
  img = Image.open(binary_data)
  print(f'angle = {angle}')
  # 当expand=True时，旋转后的图像会扩展以适应整个旋转后的图像区域，这意味着图像的尺寸会根据旋转角度进行调整，以确保旋转后的图像不会被裁剪。
  # 当expand=False（默认值）时，旋转后的图像尺寸与原始图像相同，可能会导致部分图像被裁剪。
  rotated_img = img.rotate(angle, expand=True)
  return rotated_img