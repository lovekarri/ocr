import os
import io
import json
from PIL import Image
# from utils.ocr import ocr_image_from_bytes
# from utils.util import rotate_image_with_binary_data, closed_angle_of_result, draw_red_dot_and_label_with_binary_data, draw_red_dot_and_label_with_image

from utils.ocr import ocr_image_from_bytes
from utils.util import rotate_image_with_binary_data, closed_angle_of_result, draw_red_dot_and_label_with_binary_data, draw_red_dot_and_label_with_image

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
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_101.png'), 340.83,350.83)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_102.png'), 352.37,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_103.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_104.png'), 330.85,340.0)
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
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_112.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_113.png'), 343.91,353.91)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_114.png'), 85,95)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_115.png'), 0,7.84)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_116.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_117.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_118.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_119.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_12.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_120.png'), 0,7.82)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_121.png'), 10.75,20.75)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_122.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_123.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_124.png'), 0,9.9)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_125.png'), 322.65,332.65)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_126.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_127.png'), 75.88,85.88)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_13.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_130.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_131.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_132.png'), 0,7.74)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_133.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_134.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_135.png'), 90,100.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_136.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_137.png'), 348.66,358.66)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_138.png'), 0,8.04)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_14.png'), 352.4,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_140.png'), 0,6.29)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_141.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_142.png'), 350.91,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_144.png'), 346.47,356.47)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_145.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_146.png'), 347,357.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_148.png'), 0,7.36)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_149.png'), 3,13.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_15.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_150.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_151.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_152.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_153.png'), 348.6,358.6)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_154.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_156.png'), 0,9.72)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_157.png'), 349.81,359.81)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_158.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_159.png'), 1.19,11.19)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_16.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_160.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_161.png'), 8,18)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_162.png'), 351.48,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_163.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_164.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_165.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_166.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_167.png'), 1.98,11.98)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_168.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_169.png'), 351.0,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_17.png'), 0,7.96)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_171.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_172.png'), 345.23,355.23)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_173.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_174.png'), 265,275.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_175.png'), 85,95)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_176.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_177.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_178.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_18.png'), 0.49,10.49)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_180.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_181.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_182.png'), 268.27,278.27)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_183.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_184.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_186.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_187.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_188.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_189.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_19.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_190.jpg'), 0,8.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_191.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_192.jpg'), 0,4)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_193.jpg'), 2,12.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_194.jpg'), 352.4,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_195.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_196.jpg'), 175,185.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_197.jpg'), 350,360.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_198.jpg'), 95.8,105.8)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_199.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_2.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_20.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_200.jpg'), 2.06,12.06)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_201.jpg'), 353.7,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_202.jpg'), 38,48)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_203.jpg'), 93.92,103.92)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_204.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_205.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_206.jpg'), 0,6.33)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_207.jpg'), 348.25,358.25)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_208.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_209.jpg'), 349.32,359.32)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_21.png'), 353.26,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_210.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_211.jpg'), 346.03,356.03)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_212.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_213.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_214.jpg'), 348.38,358.38)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_215.jpg'), 2.31,12.31)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_216.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_217.jpg'), 18.32,28.32)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_218.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_219.jpg'), 351.82,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_22.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_220.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_221.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_222.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_223.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_224.jpg'), 352.22,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_225.jpg'), 0,4.02)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_226.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_227.jpg'), 265,275.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_228.jpg'), 265,275.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_229.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_23.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_230.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_231.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_232.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_233.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_234.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_235.jpg'), 0,5.92)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_236.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_237.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_238.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_239.jpg'), 353.7,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_24.png'), 0,8.01)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_240.jpg'), 337.95,347.95)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_241.jpg'), 341.07,351.07)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_242.jpg'), 70.82,80.82)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_243.jpg'), 70.82,80.82)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_244.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_245.jpg'), 349.4,359.4)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_246.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_247.jpg'), 85,95)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_248.jpg'), 0,10.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_249.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_25.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_250.jpg'), 347.5,357.5)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_251.jpg'), 0,4)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_252.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_253.jpg'), 0,4)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_254.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_255.jpg'), 351.19,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_256.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_257.jpg'), 350.6,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_258.jpg'), 0.64,10.64)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_259.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_26.png'), 82.34,92.34)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_260.jpg'), 0,7.2)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_261.jpg'), 2.31,12.31)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_262.jpg'), 353.93,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_263.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_264.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_265.jpg'), 350.26,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_266.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_267.jpg'), 0,8.62)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_268.jpg'), 344.76,354.76)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_269.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_27.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_270.jpg'), 342.01,352.01)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_271.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_272.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_273.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_274.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_275.jpg'), 0,9.51)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_276.jpg'), 352.9,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_277.jpg'), 84.09,94.09)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_278.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_279.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_28.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_280.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_281.jpg'), 84.19,94.19)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_282.jpg'), 0,9.18)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_283.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_284.jpg'), 351.08,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_285.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_286.jpg'), 1.34,11.34)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_287.jpg'), 3.47,13.47)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_288.jpg'), 271.57,281.57)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_289.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_29.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_290.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_291.jpg'), 175,185.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_292.jpg'), 20,30)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_293.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_294.jpg'), 265,275)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_295.jpg'), 83.19,93.19)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_296.jpg'), 83.75,93.75)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_297.jpg'), 350.49,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_298.jpg'), 353.04,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_299.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_3.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_30.png'), 0,6.09)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_300.jpg'), 1.71,11.71)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_301.jpg'), 75,85.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_302.jpg'), 85,95.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_303.jpg'), 340,3505.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_304.jpg'), 85,95.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_305.jpg'), 338.34,348.34)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_306.jpg'), 255,265)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_307.jpg'), 275.08,285.08)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_308.jpg'), 0,6.22)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_309.jpg'), 0,7.39)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_31.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_310.jpg'), 350.36,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_311.jpg'), 351,360.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_312.jpg'), 65,75.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_313.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_314.jpg'), 265.88,275.88)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_315.jpg'), 265.88,275.88)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_316.jpg'), 325,335)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_317.jpg'), 80,90.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_318.jpg'), 20.41,30.41)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_319.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_32.png'), 353.51,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_320.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_321.jpg'), 353.89,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_322.jpg'), 0,6.47)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_323.jpg'), 15,25.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_324.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_325.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_326.jpg'), 308.25,318.25)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_327.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_328.jpg'), 352.1,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_329.jpg'), 350,360.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_33.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_330.jpg'), 0.19,10.19)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_331.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_332.jpg'), 352.11,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_333.jpg'), 350,360.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_334.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_335.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_336.jpg'), 0,9.33)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_337.jpg'), 83.68,93.68)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_338.jpg'), 350,360.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_339.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_34.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_340.jpg'), 0.78,10.78)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_341.jpg'), 349.81,359.81)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_342.jpg'), 2.99,12.99)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_343.jpg'), 1.01,11.01)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_344.jpg'), 0.19,10.19)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_345.jpg'), 0,4)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_346.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_347.jpg'), 85,95)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_348.jpg'), 77.06,87.06)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_349.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_35.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_350.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_351.jpg'), 344.99,354.99)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_352.jpg'), 0,8.62)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_353.jpg'), 15.49,25.49)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_354.jpg'), 10.22,20.22)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_355.jpg'), 328.43,338.43)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_356.jpg'), 265.13,275.13)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_357.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_358.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_359.jpg'), 350.86,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_36.png'), 0,4)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_360.jpg'), 77.21,87.21)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_361.jpg'), 304.77,314.77)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_362.jpg'), 348.96,358.96)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_363.jpg'), 1,11.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_364.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_365.jpg'), 0,9.82)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_366.jpg'), 0,10.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_367.jpg'), 0.36,10.36)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_368.jpg'), 0,8.07)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_369.jpg'), 335.56,345.56)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_37.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_370.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_371.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_372.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_373.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_374.jpg'), 0,7.31)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_375.jpg'), 353.34,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_376.jpg'), 342.44,352.44)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_377.jpg'), 346.25,356.25)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_378.jpg'), 348.77,358.77)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_379.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_38.png'), 9.25,19.25)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_380.jpg'), 13.0,23.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_381.jpg'), 7.31,17.31)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_382.jpg'), 6.8,16.8)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_383.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_384.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_385.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_386.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_387.jpg'), 5.3,15.3)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_388.jpg'), 6.04,16.04)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_389.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_39.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_390.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_391.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_392.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_393.jpg'), 341.2,351.2)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_394.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_395.jpg'), 8.67,18.67)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_396.jpg'), 47.57,57.57)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_397.jpg'), 350.68,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_398.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_399.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_4.png'), 345.0,355.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_40.png'), 0,8.09)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_400.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_401.jpg'), 352.99,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_402.jpg'), 328.08,338.08)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_403.jpg'), 7.26,17.26)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_404.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_405.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_406.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_407.jpg'), 0.88,10.88)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_408.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_409.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_41.png'), 266.58,276.58)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_410.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_411.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_412.jpg'), 342.2,352.2)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_413.jpg'), 0,7.1)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_414.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_415.jpg'), 80.79,90.79)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_416.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_417.jpg'), 4.87,14.87)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_418.jpg'), 4.21,14.21)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_419.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_42.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_420.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_421.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_422.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_423.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_424.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_426.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_427.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_428.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_429.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_43.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_430.png'), 5.38,15.38)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_431.png'), 349.37,359.37)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_433.png'), 352.69,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_434.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_435.png'), 353.19,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_436.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_439.png'), 353.13,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_44.png'), 0.57,10.57)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_440.png'), 0,8.61)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_441.png'), 348.16,358.16)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_442.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_444.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_445.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_446.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_447.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_448.png'), 0.19,10.19)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_449.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_45.png'), 0,7.34)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_450.png'), 0,8.99)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_452.png'), 8.84,18.84)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_453.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_455.png'), 343.11,353.11)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_459.png'), 0,9.89)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_46.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_462.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_463.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_465.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_468.png'), 5.01,15.01)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_47.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_471.png'), 2.77,12.77)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_472.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_477.png'), 56.44,66.44)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_48.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_482.png'), 277.26,287.26)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_483.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_486.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_49.png'), 3.25,13.25)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_491.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_492.png'), 353.21,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_494.png'), 0,8.37)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_496.png'), 0,8.04)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_497.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_499.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_5.png'), 281.0,291.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_50.png'), 343.21,353.21)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_503.png'), 351.37,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_504.png'), 0,5)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_506.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_507.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_51.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_513.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_514.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_516.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_518.png'), 346.75,356.75)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_519.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_52.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_522.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_525.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_526.png'), 348.09,358.09)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_529.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_53.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_530.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_533.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_534.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_536.png'), 353.28,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_538.png'), 1.46,11.46)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_54.png'), 340.38,350.38)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_543.png'), 351.35,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_545.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_547.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_55.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_551.png'), 353.08,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_555.png'), 297.84,307.84)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_556.png'), 4.09,14.09)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_557.png'), 353.7,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_56.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_560.png'), 13.9,23.9)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_561.png'), 0.19,10.19)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_562.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_563.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_564.png'), 15,25)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_565.png'), 4.09,14.09)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_566.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_567.png'), 0,4)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_568.png'), 4.09,14.09)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_569.png'), 0,8.61)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_57.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_571.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_572.png'), 351.34,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_573.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_574.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_575.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_576.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_577.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_578.jpg'), 325,335)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_579.jpg'), 347,357)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_58.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_580.jpg'), 0,9.3)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_581.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_582.jpg'), 13,23)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_583.jpg'), 14.5,24.5)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_584.jpg'), 109,119)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_585.jpg'), 118,128)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_586.jpg'), 138,148)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_587.jpg'), 87,97)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_588.jpg'), 350,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_589.jpg'), 350,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_59.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_590.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_591.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_592.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_593.jpg'), 344.85,354.85)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_594.jpg'), 0,8.56)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_595.jpg'), 265,275)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_596.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_597.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_598.jpg'), 105,115)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_599.jpg'), 105,115)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_6.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_60.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_600.jpg'), 105,115)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_601.jpg'), 90,100)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_602.jpg'), 90,100)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_603.jpg'), 351.02,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_604.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_605.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_606.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_607.jpg'), 0,8.61)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_608.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_609.jpg'), 105,115)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_61.png'), 0.19,10.19)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_610.jpg'), 340,350)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_611.jpg'), 345,355)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_612.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_613.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_614.jpg'), 337,347)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_615.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_616.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_617.jpg'), 337,347)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_618.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_619.jpg'), 347,357)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_62.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_620.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_621.jpg'), 0.84,10.84)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_63.png'), 348.5,358.5)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_64.png'), 352.16,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_65.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_66.png'), 347.01,357.01)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_67.png'), 0,6.75)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_68.png'), 343.91,353.91)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_69.png'), 268.18,278.18)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_7.png'), 344.22,354.22)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_70.png'), 0,7.39)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_71.png'), 0,6.33)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_72.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_73.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_74.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_75.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_76.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_77.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_78.png'), 0,4.38)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_79.png'), 30.87,40.87)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_8.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_80.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_81.png'), 25.96,35.96)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_82.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_83.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_84.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_85.png'), 346.47,356.47)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_86.png'), 351.63,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_87.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_88.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_89.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_9.png'), 352.23,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_90.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_91.png'), 82.85,92.85)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_92.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_93.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_94.png'), 6.82,16.82)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_95.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_96.png'), 351.27,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_97.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_98.png'), 0,9.72)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_99.png'), 348.29,358.29)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_1.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_10.png'), 0,7.45)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_100.png'), 20,30)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_101.png'), 351.49,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_102.png'), 353.22,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_104.png'), 25,35)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_105.jpg'), 267.0,277.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_106.jpg'), 351.59,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_107.jpg'), 175,185)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_108.jpg'), 85,95)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_109.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_11.png'), 0,6.44)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_110.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_111.jpg'), 80,90)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_112.jpg'), 265,275)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_113.jpg'), 205,215)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_114.jpg'), 250,260)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_115.jpg'), 265,275)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_116.jpg'), 350,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_117.jpg'), 340,350)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_118.jpg'), 0,7.58)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_119.jpg'), 343.94,353.94)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_12.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_120.jpg'), 6.77,16.77)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_121.jpg'), 175,185)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_122.jpg'), 351.39,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_123.jpg'), 351.05,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_124.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_125.jpg'), 0,7.69)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_126.jpg'), 309.29,319.29)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_127.jpg'), 325,335)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_128.jpg'), 0,6.57)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_129.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_13.png'), 325.19,335.19)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_130.jpg'), 0,6.99)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_131.jpg'), 349.74,359.74)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_132.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_133.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_134.jpg'), 353.59,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_135.jpg'), 352.71,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_136.jpg'), 185,195)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_137.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_138.jpg'), 0,6.53)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_139.jpg'), 0,6.29)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_14.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_140.jpg'), 0,4.01)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_141.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_142.jpg'), 265,275)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_143.jpg'), 75,85)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_144.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_145.jpg'), 351.34,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_146.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_147.jpg'), 0,5)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_148.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_149.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_15.png'), 3.62,13.62)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_150.jpg'), 260,270)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_151.jpg'), 0,5)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_152.jpg'), 353.57,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_153.jpg'), 351.39,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_154.jpg'), 0,6.79)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_155.jpg'), 0,6.08)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_156.jpg'), 0,4)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_157.jpg'), 6.61,16.61)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_158.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_159.jpg'), 265,275)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_16.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_160.jpg'), 265,275)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_161.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_162.jpg'), 85,95)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_163.jpg'), 35,45)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_164.jpg'), 90,100)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_165.jpg'), 85,95)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_166.jpg'), 0,5)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_167.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_168.jpg'), 315,325)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_169.jpg'), 255,265)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_17.png'), 0,8.61)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_170.jpg'), 1.22,11.22)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_171.jpg'), 6.75,16.75)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_172.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_173.jpg'), 350.65,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_174.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_175.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_176.jpg'), 0,7.66)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_177.jpg'), 282.68,292.68)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_178.jpg'), 2.05,12.05)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_179.jpg'), 0.1,10.1)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_18.png'), 65,75)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_180.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_181.jpg'), 351.02,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_182.jpg'), 85,95)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_183.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_184.jpg'), 352.9,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_185.jpg'), 0,6.35)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_186.jpg'), 0,7.34)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_187.jpg'), 0,7.7)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_188.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_189.jpg'), 2.34,12.34)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_19.png'), 349.81,359.81)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_190.jpg'), 305,315)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_191.jpg'), 305,315)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_192.jpg'), 7.71,17.71)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_193.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_194.jpg'), 3.03,13.03)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_195.jpg'), 79.14,89.14)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_196.jpg'), 265,275)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_197.jpg'), 160,170)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_198.jpg'), 45,55)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_199.jpg'), 347.64,357.64)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_2.png'), 0,7.69)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_20.png'), 85,95)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_200.jpg'), 352.12,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_201.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_202.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_203.jpg'), 0,6.6)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_204.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_205.jpg'), 0,9.55)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_206.jpg'), 275.78,285.78)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_207.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_208.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_209.jpg'), 0.06,10.06)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_21.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_210.jpg'), 83.89,93.89)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_211.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_212.jpg'), 353.85,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_213.jpg'), 344.05,354.05)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_214.jpg'), 313.68,323.68)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_215.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_216.jpg'), 82.5,92.5)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_217.jpg'), 15,25)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_218.jpg'), 0,5.93)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_219.jpg'), 0,8.96)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_22.png'), 0,5.83)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_220.jpg'), 0,7.63)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_221.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_222.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_223.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_224.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_225.jpg'), 265,275)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_226.jpg'), 265,275)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_227.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_228.jpg'), 85,95)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_229.jpg'), 0,6.85)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_23.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_230.jpg'), 265,275)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_231.jpg'), 1.05,11.05)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_232.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_233.jpg'), 350.64,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_234.jpg'), 0,7.43)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_235.jpg'), 0,5)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_236.jpg'), 180,190)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_237.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_238.jpg'), 270,280)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_239.jpg'), 0,7.12)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_24.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_240.jpg'), 0,10)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_241.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_242.jpg'), 348.29,358.29)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_243.jpg'), 10.21,20.21)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_244.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_245.jpg'), 65,75)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_246.jpg'), 1.57,11.57)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_247.jpg'), 0,6.9)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_248.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_249.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_25.png'), 339.58,349.58)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_250.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_251.jpg'), 0,5.77)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_252.jpg'), 0,7.96)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_253.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_254.jpg'), 0,7.86)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_255.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_256.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_257.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_258.jpg'), 0,7.75)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_259.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_26.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_260.jpg'), 353.89,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_261.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_262.jpg'), 0,9.86)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_263.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_264.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_265.jpg'), 29.26,39.26)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_266.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_267.jpg'), 0,5.93)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_268.jpg'), 346.67,356.67)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_269.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_27.png'), 85,95)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_270.jpg'), 0,7.9)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_271.jpg'), 351.09,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_272.jpg'), 83.21,93.21)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_273.jpg'), 0,9.57)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_274.jpg'), 6.08,16.08)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_275.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_276.jpg'), 0,5.87)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_277.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_278.jpg'), 8.85,18.85)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_279.jpg'), 8.28,18.28)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_28.png'), 0,7.11)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_280.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_281.jpg'), 350.72,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_282.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_283.jpg'), 261,271)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_284.jpg'), 175,185)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_285.jpg'), 265,275)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_286.jpg'), 265,275)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_287.jpg'), 255,265)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_288.jpg'), 0,6.95)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_289.jpg'), 352.76,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_29.png'), 352.88,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_290.jpg'), 35,45)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_291.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_292.jpg'), 351.29,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_293.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_294.jpg'), 353.87,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_295.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_296.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_297.jpg'), 0,8.26)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_298.jpg'), 80,90)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_299.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_3.png'), 352.61,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_30.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_300.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_301.jpg'), 3.13,13.13)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_302.jpg'), 170,180)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_303.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_304.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_305.jpg'), 255,265)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_306.jpg'), 0,8.15)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_307.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_308.jpg'), 5.71,15.71)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_309.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_31.png'), 0,6.29)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_310.jpg'), 0,6.31)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_311.jpg'), 0,5)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_312.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_313.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_314.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_315.jpg'), 0,9.86)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_316.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_317.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_318.jpg'), 285,295)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_319.jpg'), 1,11)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_32.png'), 0,10)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_320.jpg'), 352.55,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_321.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_322.jpg'), 0,6.62)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_323.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_324.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_325.jpg'), 10.71,20.71)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_326.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_327.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_328.jpg'), 85,95)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_329.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_33.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_330.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_331.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_332.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_333.jpg'), 0,5.89)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_334.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_335.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_336.jpg'), 85,95)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_337.jpg'), 352.5,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_338.jpg'), 350,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_339.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_34.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_340.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_341.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_342.jpg'), 85,95)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_343.jpg'), 0,8.5)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_344.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_345.jpg'), 353.14,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_346.jpg'), 0,5)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_347.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_348.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_35.png'), 85,95)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_350.png'), 350.31,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_351.png'), 1.71,11.71)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_352.png'), 353.3,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_354.png'), 40,50)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_355.png'), 0,5.92)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_356.png'), 347,357)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_357.png'), 0,8)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_36.png'), 351.86,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_360.png'), 353.5,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_361.png'), 55,65)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_362.png'), 0,6.68)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_363.png'), 0,4.09)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_365.png'), 345,355)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_366.png'), 351.84,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_368.png'), 5,15)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_37.png'), 0,4.43)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_372.png'), 0,5)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_373.png'), 347,357)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_38.png'), 0,4)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_380.png'), 60,70)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_384.png'), 0,5)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_389.png'), 0,7.64)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_39.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_391.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_392.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_397.png'), 353.13,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_399.png'), 325,335)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_4.png'), 1.77,11.77)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_40.png'), 65,75)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_401.png'), 2.13,12.13)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_404.png'), 351.86,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_407.png'), 353.39,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_41.png'), 0,6.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_42.png'), 0,6.86)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_421.png'), 351.63,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_427.png'), 0,9.46)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_43.png'), 352.21,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_434.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_44.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_440.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_442.png'), 83.97,93.97)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_445.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_45.png'), 337,347)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_452.png'), 352.34,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_455.png'), 5,15)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_46.png'), 8.39,18.39)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_464.png'), 348.08,358.08)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_47.png'), 3.6,13.6)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_472.png'), 0,8.62)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_475.jpg'), 335,345)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_476.jpg'), 325,335)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_477.jpg'), 268.06,278.06)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_478.jpg'), 351.84,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_479.jpg'), 11.63,21.63)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_48.png'), 342.17,352.17)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_480.jpg'), 330.51,340.51)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_481.jpg'), 343,353)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_49.png'), 0,5)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_5.png'), 345.13,355.13)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_50.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_51.png'), 280.46,290.46)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_52.png'), 349.06,359.06)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_53.png'), 352.49,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_54.png'), 351.23,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_55.png'), 15.04,25.04)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_56.png'), 21,31)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_57.png'), 0,6.24)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_58.png'), 40,50)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_59.png'), 0,7.73)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_6.png'), 0,6.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_60.png'), 0,7.45)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_61.png'), 352.51,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_62.png'), 5,15)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_63.png'), 0,5)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_67.png'), 352.69,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_68.png'), 7.76,17.76)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_69.png'), 0,5)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_7.png'), 85,95)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_70.png'), 353.97,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_72.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_73.png'), 0,6.75)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_74.png'), 352.75,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_75.png'), 82.33,92.33)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_76.png'), 0,10)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_77.png'), 0,10)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_79.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_8.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_80.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_81.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_82.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_83.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_85.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_86.png'), 0,5)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_87.png'), 0,9.57)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_88.png'), 351.35,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_9.png'), 0,8.51)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_90.png'), 15,25)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_91.png'), 33.66,43.66)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_92.png'), 0,9.33)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_94.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_95.png'), 33.33,43.33)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_96.png'), 352.83,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_97.png'), 0,6.09)
    True
    >>> is_between(find_correct_angle('/paddle/blood_sugar/blood_sugar_99.png'), 0,5.0)
    True
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
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_112.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_113.png'), 343.91,353.91)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_114.png'), 85,95)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_115.png'), 0,7.84)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_116.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_117.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_118.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_119.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_12.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_120.png'), 0,7.82)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_121.png'), 3.75,13.75)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_122.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_123.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_124.png'), 0,9.9)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_125.png'), 327.65,337.65)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_126.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_127.png'), 75.88,85.88)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_13.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_130.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_131.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_132.png'), 0,7.74)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_133.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_134.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_135.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_136.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_137.png'), 348.66,358.66)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_138.png'), 0,8.04)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_14.png'), 352.4,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_140.png'), 0,6.29)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_141.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_142.png'), 350.91,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_144.png'), 346.47,356.47)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_145.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_146.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_148.png'), 0,7.36)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_149.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_15.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_150.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_151.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_152.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_153.png'), 348.6,358.6)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_154.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_156.png'), 0,9.72)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_157.png'), 349.81,359.81)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_158.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_159.png'), 1.19,11.19)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_16.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_160.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_161.png'), 0,4)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_162.png'), 351.48,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_163.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_164.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_165.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_166.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_167.png'), 1.98,11.98)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_168.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_169.png'), 351.0,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_17.png'), 0,7.96)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_171.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_172.png'), 345.23,355.23)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_173.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_174.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_175.png'), 85,95)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_176.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_177.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_178.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_18.png'), 0.49,10.49)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_180.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_181.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_182.png'), 82.27,92.27)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_183.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_184.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_186.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_187.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_188.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_189.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_19.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_190.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_191.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_192.jpg'), 0,4)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_193.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_194.jpg'), 352.4,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_195.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_196.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_197.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_198.jpg'), 277.8,287.8)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_199.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_2.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_20.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_200.jpg'), 2.06,12.06)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_201.jpg'), 353.7,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_202.jpg'), 85,95)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_203.jpg'), 273.92,283.92)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_204.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_205.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_206.jpg'), 0,6.33)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_207.jpg'), 348.25,358.25)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_208.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_209.jpg'), 349.32,359.32)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_21.png'), 353.26,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_210.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_211.jpg'), 346.03,356.03)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_212.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_213.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_214.jpg'), 348.38,358.38)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_215.jpg'), 2.31,12.31)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_216.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_217.jpg'), 9.32,19.32)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_218.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_219.jpg'), 351.82,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_22.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_220.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_221.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_222.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_223.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_224.jpg'), 352.22,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_225.jpg'), 0,4.02)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_226.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_227.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_228.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_229.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_23.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_230.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_231.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_232.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_233.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_234.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_235.jpg'), 0,5.92)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_236.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_237.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_238.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_239.jpg'), 353.7,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_24.png'), 0,8.01)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_240.jpg'), 344.95,354.95)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_241.jpg'), 341.07,351.07)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_242.jpg'), 58.82,68.82)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_243.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_244.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_245.jpg'), 349.4,359.4)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_246.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_247.jpg'), 85,95)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_248.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_249.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_25.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_250.jpg'), 347.5,357.5)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_251.jpg'), 0,4)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_252.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_253.jpg'), 45,55)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_254.jpg'), 350,360.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_255.jpg'), 351.19,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_256.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_257.jpg'), 350.6,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_258.jpg'), 0.64,10.64)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_259.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_26.png'), 268.34,278.34)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_260.jpg'), 0,7.2)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_261.jpg'), 2.31,12.31)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_262.jpg'), 353.93,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_263.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_264.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_265.jpg'), 350.26,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_266.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_267.jpg'), 0,8.62)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_268.jpg'), 344.76,354.76)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_269.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_27.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_270.jpg'), 342.01,352.01)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_271.jpg'), 350,360.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_272.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_273.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_274.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_275.jpg'), 0,9.51)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_276.jpg'), 352.9,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_277.jpg'), 84.09,94.09)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_278.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_279.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_28.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_280.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_281.jpg'), 350.19,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_282.jpg'), 342,252.18)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_283.jpg'), 85,95.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_284.jpg'), 351.08,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_285.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_286.jpg'), 1.34,11.34)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_287.jpg'), 3.47,13.47)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_288.jpg'), 271.57,281.57)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_289.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_29.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_290.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_291.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_292.jpg'), 0,4)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_293.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_294.jpg'), 85,95)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_295.jpg'), 58.19,68.19)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_296.jpg'), 83.75,93.75)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_297.jpg'), 350.49,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_298.jpg'), 353.04,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_299.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_3.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_30.png'), 0,6.09)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_300.jpg'), 1.71,11.71)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_301.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_302.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_303.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_304.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_305.jpg'), 338.34,348.34)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_306.jpg'), 85,95)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_307.jpg'), 334.08,344.08)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_308.jpg'), 0,6.22)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_309.jpg'), 0,7.39)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_31.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_310.jpg'), 350.36,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_311.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_312.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_313.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_314.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_315.jpg'), 348.88,358.88)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_316.jpg'), 0,4)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_317.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_318.jpg'), 14.41,24.41)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_319.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_32.png'), 353.51,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_320.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_321.jpg'), 353.89,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_322.jpg'), 0,6.47)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_323.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_324.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_325.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_326.jpg'), 319.25,329.25)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_327.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_328.jpg'), 352.1,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_329.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_33.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_330.jpg'), 0.19,10.19)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_331.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_332.jpg'), 352.11,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_333.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_334.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_335.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_336.jpg'), 0,9.33)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_337.jpg'), 83.68,93.68)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_338.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_339.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_34.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_340.jpg'), 0.78,10.78)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_341.jpg'), 349.81,359.81)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_342.jpg'), 2.99,12.99)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_343.jpg'), 1.01,11.01)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_344.jpg'), 0.19,10.19)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_345.jpg'), 0,4)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_346.jpg'), 350,360.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_347.jpg'), 85,95)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_348.jpg'), 77.06,87.06)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_349.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_35.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_350.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_351.jpg'), 344.99,354.99)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_352.jpg'), 0,8.62)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_353.jpg'), 0.49,10.49)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_354.jpg'), 2.22,12.22)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_355.jpg'), 328.43,338.43)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_356.jpg'), 83.13,93.13)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_357.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_358.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_359.jpg'), 350.86,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_36.png'), 0,4)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_360.jpg'), 77.21,87.21)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_361.jpg'), 304.77,314.77)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_362.jpg'), 348.96,358.96)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_363.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_364.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_365.jpg'), 0,9.82)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_366.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_367.jpg'), 0.36,10.36)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_368.jpg'), 0,8.07)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_369.jpg'), 340.56,350.56)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_37.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_370.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_371.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_372.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_373.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_374.jpg'), 0,7.31)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_375.jpg'), 353.34,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_376.jpg'), 342.44,352.44)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_377.jpg'), 346.25,356.25)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_378.jpg'), 348.77,358.77)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_379.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_38.png'), 17.25,27.25)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_380.jpg'), 20.0,30.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_381.jpg'), 20.31,30.31)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_382.jpg'), 6.8,16.8)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_383.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_384.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_385.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_386.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_387.jpg'), 13.5,23.5)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_388.jpg'), 12.5,22.5)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_389.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_39.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_390.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_391.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_392.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_393.jpg'), 330.2,340.2)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_394.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_395.jpg'), 25,35)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_396.jpg'), 47.57,57.57)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_397.jpg'), 350.68,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_398.jpg'), 265,275)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_399.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_4.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_40.png'), 0,8.09)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_400.jpg'), 340,350)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_401.jpg'), 352.99,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_402.jpg'), 315.08,325.08)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_403.jpg'), 30,40)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_404.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_405.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_406.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_407.jpg'), 0.88,10.88)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_408.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_409.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_41.png'), 266.58,276.58)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_410.jpg'), 345,355)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_411.jpg'), 265,275)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_412.jpg'), 335.2,345.2)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_413.jpg'), 0,7.1)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_414.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_415.jpg'), 90.79,100.79)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_416.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_417.jpg'), 4.87,14.87)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_418.jpg'), 4.21,14.21)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_419.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_42.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_420.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_421.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_422.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_423.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_424.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_426.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_427.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_428.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_429.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_43.png'), 0,10.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_430.png'), 5.38,15.38)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_431.png'), 349.37,359.37)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_433.png'), 352.69,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_434.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_435.png'), 353.19,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_436.png'),330,340)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_439.png'), 353.13,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_44.png'), 0.57,10.57)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_440.png'), 0,8.61)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_441.png'), 348.16,358.16)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_442.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_444.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_445.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_446.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_447.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_448.png'), 0.19,10.19)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_449.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_45.png'), 0,7.34)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_450.png'), 0,8.99)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_452.png'), 8.84,18.84)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_453.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_455.png'), 343.11,353.11)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_459.png'), 0,9.89)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_46.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_462.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_463.png'), 90,100)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_465.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_468.png'), 88,98)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_47.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_471.png'), 2.77,12.77)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_472.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_477.png'), 56.44,66.44)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_48.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_482.png'), 100,110)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_483.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_486.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_49.png'), 3.25,13.25)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_491.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_492.png'), 353.21,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_494.png'), 0,8.37)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_496.png'), 0,8.04)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_497.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_499.png'), 90,100)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_5.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_50.png'), 343.21,353.21)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_503.png'), 351.37,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_504.png'), 3.43,13.43)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_506.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_507.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_51.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_513.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_514.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_516.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_518.png'), 346.75,356.75)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_519.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_52.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_522.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_525.png'), 340,350)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_526.png'), 348.09,358.09)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_529.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_53.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_530.png'), 90,100)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_533.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_534.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_536.png'), 353.28,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_538.png'), 1.46,11.46)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_54.png'), 65,75)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_543.png'), 351.35,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_545.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_547.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_55.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_551.png'), 353.08,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_555.png'), 297.84,307.84)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_556.png'), 4.09,14.09)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_557.png'), 353.7,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_56.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_560.png'), 13.9,23.9)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_561.png'), 0.19,10.19)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_562.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_563.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_564.png'), 2.59,12.59)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_565.png'), 4.09,14.09)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_566.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_567.png'), 0,4)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_568.png'), 4.09,14.09)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_569.png'), 0,8.61)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_57.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_571.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_572.png'), 351.34,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_573.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_574.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_575.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_576.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_577.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_578.jpg'), 346.47,356.47)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_579.jpg'), 0,4.22)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_58.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_580.jpg'), 0,9.3)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_581.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_582.jpg'), 8.57,18.57)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_583.jpg'), 9.45,19.45)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_584.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_585.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_586.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_587.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_588.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_589.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_59.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_590.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_591.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_592.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_593.jpg'), 344.85,354.85)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_594.jpg'), 0,8.56)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_595.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_596.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_597.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_598.jpg'), 274.67,284.67)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_599.jpg'), 279.04,289.04)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_6.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_60.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_600.jpg'), 353.8,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_601.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_602.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_603.jpg'), 351.02,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_604.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_605.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_606.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_607.jpg'), 0,8.61)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_608.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_609.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_61.png'), 0.19,10.19)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_610.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_611.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_612.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_613.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_614.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_615.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_616.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_617.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_618.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_619.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_62.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_620.jpg'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_621.jpg'), 0.84,10.84)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_63.png'), 348.5,358.5)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_64.png'), 352.16,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_65.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_66.png'), 330.01,340.01)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_67.png'), 0,6.75)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_68.png'), 327.91,337.91)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_69.png'), 337.18,347.18)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_7.png'), 344.22,354.22)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_70.png'), 0,7.39)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_71.png'), 0,6.33)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_72.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_73.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_74.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_75.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_76.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_77.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_78.png'), 0,4.38)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_79.png'), 35.87,45.87)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_8.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_80.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_81.png'), 30.96,40.96)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_82.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_83.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_84.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_85.png'), 346.47,356.47)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_86.png'), 351.63,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_87.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_88.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_89.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_9.png'), 352.23,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_90.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_91.png'), 82.85,92.85)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_92.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_93.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_94.png'), 6.82,16.82)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_95.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_96.png'), 351.27,360)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_97.png'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_98.png'), 0,9.72)
    True
    >>> is_between(find_correct_angle('/paddle/blood_pressure/blood_pressure_99.png'), 345.29,355.29)
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