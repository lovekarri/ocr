import os
import io
import json
from PIL import Image
# from utils.ocr import ocr_image_from_bytes
# from utils.util import rotate_image_with_binary_data, closed_angle_of_result, draw_red_dot_and_label_with_binary_data, draw_red_dot_and_label_with_image

from ocr import ocr_image_from_bytes
from util import rotate_image_with_binary_data, closed_angle_of_result, draw_red_dot_and_label_with_binary_data, draw_red_dot_and_label_with_image

OCR_SAVE_DIRECTORY = "/paddle/images/ocr"

IMAGE_PATH = '/paddle/ocr/res/'


def path_with_image_name(image_name):
    return os.path.join(IMAGE_PATH, image_name)


def load_img_with_name(image_name):
    image_path = path_with_image_name(image_name)
    with open(image_path, 'rb') as f:
        return f.read()



#
# filename: 原始文件名
# anglevalue: 旋转的角度，如果为-1则为该图片未识别成功，未旋转
# clockwise: 1为顺时针旋转，-1为逆时针旋转
# original: 原图ocr识别结果
# rotated: 原图旋转anglevalue角度后重新ocr识别的结果
def final_result(code, file_name, angle_value, clock_wise, original_result, rotated_result):
    return {
        'status': code,
        'result': {
            'filename': file_name,
            'anglevalue': angle_value,
            'clockwise': clock_wise,
            'original': original_result,
            'rotated': rotated_result
        }
    }


def draw_and_save_image(image_bytes, result, file_path):
    if len(result) == 0:
        Image.open(image_bytes).save(file_path)
    else:
        # 在图片上标注识别出的坐标信息
        original_img = draw_red_dot_and_label_with_binary_data(image_bytes , result)
        # 将图片保存到指定目录
        original_img.save(file_path, format='PNG')


# 如果anglevalue > 0，需要逆时针旋转，如果anglevalue < 0，需要顺时针旋转
def clockwise_with_anglevalue(anglevalue):
    if anglevalue < 0:
        return 1
    else:
        return 0


def rotated_file_path_with_anglevalue(file_name):
    # if anglevalue < 0:
    #     rotated = 'clockwise'
    # else:
    #     rotated = 'anticlockwise'
    rotated_file_name = os.path.splitext(file_name)[0] + '_rotated.png'
    path = os.path.join(OCR_SAVE_DIRECTORY, rotated_file_name) 
    # print(f'rotated_file_path = {path}')
    return path


def ocr_result_with_image_bytes(binary_data, file_name):
    result = ocr_image_from_bytes(binary_data, True, 'ch')
    file_path = os.path.join(OCR_SAVE_DIRECTORY, file_name)
    draw_and_save_image(io.BytesIO(binary_data), result, file_path)
    return result


def ocr_result_after_rotate_with_image_bytes(binary_data, file_path, vv):
    
    img = rotate_image_with_binary_data(io.BytesIO(binary_data), vv)
    byte_io = io.BytesIO()
    img.save(byte_io, format='PNG')
    image_bytes = byte_io.getvalue()
    result = ocr_image_from_bytes(image_bytes, False, 'ch')
    rotated_image = draw_red_dot_and_label_with_image(img, result)
    rotated_image.save(file_path, format='PNG')
    
    return result


def response_data_with_binary_data(binary_data, file_name):
    
    result = ocr_result_with_image_bytes(binary_data, file_name)
    
    if len(result) == 0:
        # 返回结果
        return final_result(200, file_name, -1, -1, result, [])
    else:
    
        # 距离其他偏转角度最近的角度
        anglevalue = closed_angle_of_result(result)

        # 角度 < 1 直接返回，不进行旋转
        if abs(anglevalue) < 1:
            return final_result(200, file_name, anglevalue, -1, result, [])

        # 图片旋转方法rotate_image_with_binary_data的参数vv为负值，将图片顺时针旋转；vv为正值，将图片逆时针旋转
        vv = anglevalue
        if anglevalue < 0:
            vv =  anglevalue + 360
        # clockwise = clockwise_with_anglevalue(vv)
        rotated_result = ocr_result_after_rotate_with_image_bytes(binary_data, rotated_file_path_with_anglevalue(file_name), vv)

        # 虽然此处直接返回了，还可以向后延伸
        # rotated_result是旋转后再次识别的结果，本次识别未开启文字方向识别器。
        # 如果识别效果很差，则将其旋转180°后应该方向正确
        # 此时关闭文字方向识别器再次识别文字，识别结果与第一次相近或者更好
        return final_result(200, file_name, vv, -1, result, rotated_result)
    


def load_img_with_path(fpath):
    with open(fpath, 'rb') as f:
        return f.read()


def find_correct_angle(fpath):

    binary_data = load_img_with_path(fpath)

    file_name = os.path.basename(fpath)
    result = response_data_with_binary_data(binary_data, file_name)
    # TODO: 从result中获取角度，返回。
    anglevalue = result['result']['anglevalue']
    # print(f'anglevalue = {anglevalue}')
    return anglevalue

def is_between(v, start, end, include_equal=True):
    # '''
    # >>> is_between(1, 1, 2)
    # True
    # >>> is_between(1, 1, 2, False)
    # False
    # >>> is_between(1, 6, 2)
    # False
    # >>> is_between(1, 6, 2, False)
    # False
    # '''
    '''
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_1.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_10.png'), 0.08,10.08)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_100.png'), 1.34,11.34)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_101.png'), 348.83,358.83)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_102.png'), 352.37,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_103.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_104.png'), 351.85,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_105.png'), 0,9.54)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_106.png'), 9.65,19.65)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_107.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_108.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_109.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_11.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_110.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_111.png'), 0,5.0)
    True
    '''
    if include_equal:
        return v <= max(start, end) and v >= min(start, end)
    return v < max(start, end) and v > min(start, end)


if __name__ == '__main__':
    import doctest
    print(doctest.testmod(verbose=False, report=False))


# if __name__ == '__main__':
#     import sys
#     if len(sys.argv) > 1:
#         find_correct_angle(sys.argv[1])
#     else:
#         find_correct_angle('/paddle/blood_pressure/blood_pressure_111.png')