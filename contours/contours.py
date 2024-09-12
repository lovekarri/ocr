import cv2
import io
import os

from PIL import Image
from pathlib import Path
# from sklearn.cluster import KMeans

from pathlib import Path
import json
import time
import sys

import numpy as np
# from utils.image import is_image


# DEFAULT_PATH = '/Users/samguo/Downloads/houghlines/test1/resources'
# RESULT_PATH = '/Users/samguo/Downloads/houghlines/test1/result'
# JSON_PATH = '/Users/samguo/Downloads/houghlines/test1/json'
# DEFAULT_PATH = '/Users/samguo/Workspace/resources/new_pressure'
DEFAULT_PATH = '/Users/samguo/Workspace/resources/new_sugar'
RESULT_PATH = '/Users/samguo/Workspace/resources/result'
JSON_PATH = '/Users/samguo/Workspace/resources/json'


def testit(file_path=None):

    if file_path is None:
        print("没有提供文件路径参数，使用默认路径。")
        file_path = DEFAULT_PATH

    images = os.listdir(file_path)

    total_time = 0
    image_count = 0

    for image_name in images:
        start_time = time.time()
        
        full_path = os.path.join(file_path, image_name)
        if is_image(full_path) == False:
            continue
        image_count += 1
        # analyze_image_and_save_result_to_path(full_path)
        color_ract_of_image(full_path)
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        total_time += elapsed_time

    average_time = total_time / image_count
    print(f"Average time for all {image_count} APIs call: {average_time:.4f} seconds.")




def testit_with_filed_files(file_path=None):

    if file_path is None:
        print("没有提供文件路径参数，使用默认路径。")
        file_path = DEFAULT_PATH

    images = os.listdir(file_path)

    total_time = 0
    image_count = 0

    for image_name in images:
        start_time = time.time()
        
        full_path = os.path.join(DEFAULT_PATH, image_name)
        if is_image(full_path) == False:
            continue
        image_count += 1
        # analyze_image_and_save_result_to_path(full_path)
        color_ract_of_image(full_path)
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        total_time += elapsed_time

    average_time = total_time / image_count
    print(f"Average time for all {image_count} APIs call: {average_time:.4f} seconds.")



def analyze_image_and_save_result_to_path(fpath):

    image = color_ract_of_image(fpath)
    image_name = os.path.basename(fpath)
    save_path = os.path.join(RESULT_PATH, image_name)
    cv2.imwrite(save_path, image)


def is_image(file_path):
    extension = os.path.splitext(file_path)[1].lower()
    return extension in ['.jpg', '.png', '.jpeg']

















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



# 可以明确辨识的颜色区域
def color_of_hsv() -> list:
    orange_lower = np.array([11, 100, 100])
    orange_upper = np.array([25, 255, 255])
    green_lower = np.array([40, 100, 100])
    green_upper = np.array([80, 255, 255])
    blue_lower = np.array([95, 30, 150])
    blue_upper = np.array([115, 70, 255])
    blue_lower2 = np.array([65, 5, 150])
    blue_upper2 = np.array([100, 35, 255])
    red_lower = np.array([0, 100, 100])
    red_upper = np.array([10, 255, 255])
    red_lower2 = np.array([165, 90, 90])
    red_upper2 = np.array([180, 255, 255])

    color_ranges = [
        (orange_lower, orange_upper, 'orange'), 
        (green_lower, green_upper, 'green'),
        (blue_lower, blue_upper, 'blue1'),
        (blue_lower2, blue_upper2, 'blue2'),
        (red_lower, red_upper, 'blue1'),
        (red_lower2, red_upper2, 'blue2'),
                    ]
    return color_ranges


# 低饱和度、低亮度、低色相区域
def low_of_hsv() -> list:
    light_lower = np.array([0, 0, 0])
    light_upper = np.array([180, 255, 50])
    saturation_lower = np.array([0, 0, 0])
    saturation_upper = np.array([180, 50, 255])
    color_lower = np.array([0, 0, 0])
    color_upper = np.array([30, 255, 255])

    color_ranges = [
        (light_lower, light_upper, 'light'), 
        # (color_lower, color_upper, 'color'),
        (saturation_lower, saturation_upper, 'saturation'),
                    ]
    return color_ranges


# 中低饱和度、中低亮度、中低色相区域
def low_middle_of_hsv() -> list:
    light_lower = np.array([0, 0, 0])
    light_upper = np.array([180, 255, 100])
    saturation_lower = np.array([0, 0, 0])
    saturation_upper = np.array([180, 100, 255])
    color_lower = np.array([0, 0, 0])
    color_upper = np.array([70, 255, 255])

    color_ranges = [
        (light_lower, light_upper, 'light'), 
        # (color_lower, color_upper, 'color'),
        (saturation_lower, saturation_upper, 'saturation'),
                    ]
    return color_ranges

# 中高饱和度、中高亮度、中高色相区域
def middle_high_of_hsv() -> list:
    light_lower = np.array([0, 0, 100])
    light_upper = np.array([180, 255, 200])
    saturation_lower = np.array([0, 100, 0])
    saturation_upper = np.array([180, 200, 255])
    color_lower = np.array([0, 0, 150])
    color_upper = np.array([180, 255, 255])

    color_ranges = [
        (light_lower, light_upper, 'light'), 
        (color_lower, color_upper, 'color'),
        (saturation_lower, saturation_upper, 'saturation'),
                    ]
    return color_ranges


# 高饱和度、高亮度、高色相区域
def high_of_hsv() -> list:
    light_lower = np.array([0, 0, 200])
    light_upper = np.array([180, 255, 255])
    color_lower = np.array([0, 200, 0])
    color_upper = np.array([180, 255, 255])
    saturation_lower = np.array([130, 0, 0])
    saturation_upper = np.array([180, 255, 255])

    color_ranges = [
        (light_lower, light_upper, 'light'), 
        (color_lower, color_upper, 'color'),
        (saturation_lower, saturation_upper, 'saturation'),
                    ]
    return color_ranges


# 高饱和度、高亮度、高色相区域
def special_hsv() -> list:
    light_lower = np.array([0, 0, 80])
    light_upper = np.array([100, 100, 140])
    color_lower = np.array([40, 100, 100])
    color_upper = np.array([90, 255, 255])
    saturation_lower = np.array([0, 0, 150])
    saturation_upper = np.array([180, 50, 200])

    color_ranges = [
        (light_lower, light_upper, 'light'), 
        # (color_lower, color_upper, 'color'),
        # (saturation_lower, saturation_upper, 'saturation'),
                    ]
    return color_ranges


def color_ract_of_image(fpath: str='/Users/samguo/Downloads/blood_pressure_127.png'):
    
    local_file = Path(fpath)
    content = local_file.read_bytes()
    bytesio = io.BytesIO(content)
    pil_image = Image.open(bytesio)
    np_image = pil_image_to_cv2_image(pil_image)
    hsv_image = cv2.cvtColor(np_image, cv2.COLOR_BGR2HSV)

    height, width = np_image.shape[:2]
    long_edge_image = max(width, height)
    short_edge_image = min(width, height)

    color_ranges = [
        # color_of_hsv(),
        # low_of_hsv(),
        # high_of_hsv(),
        # low_middle_of_hsv(),
        # middle_high_of_hsv(),
        special_hsv()
    ]

    for ranges in color_ranges:
        # 保存过滤后的轮廓
        selected_contours = []
        screen_contour = {}
        for lower, upper, color_name in ranges:
            mask = cv2.inRange(hsv_image, lower, upper)
            contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            print(f'contours.count = {len(contours)}, color = {color_name}')

            new_contours = []
            for i, cnt in enumerate(contours):
                parent_idx = hierarchy[0][i][3]
                if parent_idx == -1:
                    new_contours.append(cnt)
            if len(new_contours) > 0:
                screen_contour[color_name] = {
                    'contours': max(new_contours, key=cv2.contourArea),
                    'lower': lower,
                    'upper': upper
                }
        keys = screen_contour.keys()
        if len(keys) > 0:
            for key in keys:
                contours = screen_contour[key]['contours']
                area = cv2.contourArea(contours)
                rect = cv2.minAreaRect(contours)

                '''
                过滤掉长宽基本与图片相等的
                '''
                rect_width, rect_height = rect[1]
                long_edge_rect = max(rect_width, rect_height)
                short_edge_rect = min(rect_width, rect_height)
                is_width_equal = abs(short_edge_image - short_edge_rect) < 0.05 * short_edge_image
                is_height_equal = abs(long_edge_image - long_edge_rect) < 0.05 * long_edge_image
                if is_width_equal and is_height_equal:
                    print(f'too like original image')
                    continue
                
                '''
                过滤掉长宽都不足屏幕1/10的
                '''
                is_width_too_small = abs(short_edge_image - short_edge_rect) > 0.9 * short_edge_image
                is_height_too_small = abs(long_edge_image - long_edge_rect) > 0.9 * long_edge_image
                if is_width_too_small and is_height_too_small:
                    print(f'too like original image')
                    continue

                '''
                过滤掉轮廓面积与最小外接矩形面积相差太大的
                '''
                area_rect = rect[1][0] * rect[1][1]
                if area_rect <= 0:
                    print(f'area_rect <= 0')
                    continue
                if area / area_rect < 0.75:
                    print(f'area / area_rect < 0.7')
                    continue

                '''
                剩余的轮廓保存到list中
                '''
                selected_contours.append({
                    'rect': rect,
                    'contours': contours,
                    'lower': screen_contour[key]['lower'],
                    'upper':  screen_contour[key]['upper']
                })
                print(f'rect = {rect}')

        # 如果未找到合适的轮廓，直接开启下一轮
        if len(selected_contours) == 0:
            continue

        # 有合适的轮廓，将其显示出来，退出循环
        max_area = 0
        largest_rectangle = None
        for item in selected_contours:
            rect = item['rect']
            area = rect[1][0] * rect[1][1]
            if area > max_area:
                max_area = area
                largest_rectangle = item
        print(f'selected_contours 1111 = {selected_contours}')
        points = cv2.boxPoints(largest_rectangle['rect'])
        points = np.int0(points)
        print(f'largest_rectangle = {largest_rectangle}')
        print(f'points = {points}')
        cv2.drawContours(np_image, [largest_rectangle['contours']], -1, (255, 0, 255), 2)
        cv2.polylines(np_image, [points], -1, (0,0,255), 3)


        # image = color_ract_of_image(fpath)
        image_name = os.path.basename(fpath)
        save_path = os.path.join(RESULT_PATH, image_name)
        cv2.imwrite(save_path, np_image)
        target_contours = largest_rectangle['contours']
        serializable_contours = [contour.tolist() for contour in target_contours]
        target_rect = largest_rectangle['rect']
        serializable_rect = [[target_rect[0][0], target_rect[0][1]], [target_rect[1][0], target_rect[1][1]]]
        dict = {
            'name': image_name,
            'input': {
                'format': 'hsv',
                'lower': largest_rectangle['lower'].tolist(),
                'upper': largest_rectangle['upper'].tolist(),
            },
            'output':{
                'rect': serializable_rect,
                'contours': serializable_contours
            }
        }
        list = image_name.split('.')
        json_name = list[0] + '.json'
        json_path = os.path.join(JSON_PATH, json_name)

        json_name = os.path.splitext(image_name)[0] + '.json'
        json_path = os.path.join(JSON_PATH, json_name)
        if not os.path.exists(json_path):
            open(json_path, 'a').close()
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(dict, f, ensure_ascii=False, indent=4)

        break

    # 显示结果图像
    # cv2.imshow('Blood Pressure Screen', np_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return np_image






if __name__ == '__main__':
    if len(sys.argv) > 1:
        # color_ract_of_image(sys.argv[1])
        # testit(sys.argv[1])
        testit_with_filed_files(sys.argv[1])
    else:
        # color_ract_of_image()
        # testit()
        testit_with_filed_files()