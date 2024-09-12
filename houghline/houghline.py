import cv2
import io

from PIL import Image
from pathlib import Path
# from sklearn.cluster import KMeans

import numpy as np

# from utils.image import image_to_gray_image, canny_edges_of_image, pil_image_to_cv2_image

    
        
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



def hough_line_with_bytesio(image: np.ndarray) -> list:
    
    gray = image_to_gray_image(image)
    edges = canny_edges_of_image(gray)
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)

    return lines

# for循环提取直线
def filter_hough_lines(lines, angle_threshold=5, distance_threshold=10):
    filtered_lines = []
    index = 0
    for line in lines:
        rho, theta = line[0]
        add_line = True
        for filtered_line in filtered_lines:
            print(f'index = {index}')
            index += 1
            filtered_rho, filtered_theta = filtered_line
            angle_diff = abs(theta - filtered_theta)
            if angle_diff < np.radians(angle_threshold):
                distance_diff = abs(rho - filtered_rho)
                if distance_diff < distance_threshold:
                    add_line = False
                    break
        if add_line:
            filtered_lines.append((rho, theta))
    return filtered_lines


def filter_dense_lines(image, lines, threshold):
    # 统计直线在图像中的分布情况
    line_counts = np.zeros(image.shape[:2], dtype=np.int32)
    for line in lines:
        rho, theta = line[0]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))
        cv2.line(line_counts, (x1, y1), (x2, y2), 1, 2)

    # 根据阈值筛选密集直线
    dense_lines = []
    for line in lines:
        rho, theta = line[0]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))

        # 统计该直线上的像素点数
        line_pixel_count = np.sum(line_counts[y1:y2, x1:x2])
        if line_pixel_count > threshold:
            dense_lines.append(line)

    return dense_lines



def merge_close_lines(np_lines, threshold_distance):
    print(f'lines = {len(np_lines)}')
    lines = list(np_lines)
    merged_lines = []
    while lines:
        current_line = lines.pop(0)
        similar_lines = [current_line]
        for line in lines:
            x1_1, y1_1, x2_1, y2_1 = current_line[0]
            x1_2, y1_2, x2_2, y2_2 = line[0]
            dist1 = np.linalg.norm(np.array([x1_1, y1_1]) - np.array([x1_2, y1_2]))
            dist2 = np.linalg.norm(np.array([x2_1, y2_1]) - np.array([x2_2, y2_2]))
            avg_dist = (dist1 + dist2) / 2
            if avg_dist < threshold_distance:
                similar_lines.append(line)
        merged_line = np.mean(similar_lines, axis=0).astype(np.int32)[0]
        merged_lines.append(merged_line)
    return np.array(merged_lines)


def merge_similar_lines(np_lines):
    merged_lines = []
    lines = list(np_lines)
    while lines:
        current_line = lines.pop(0)
        similar_lines = [current_line]
        x1_1, y1_1, x2_1, y2_1 = current_line
        for line in lines:
            x1_2, y1_2, x2_2, y2_2 = line
            # 计算角度
            angle1 = np.arctan2(y2_1 - y1_1, x2_1 - x1_1)
            angle2 = np.arctan2(y2_2 - y1_2, x2_2 - x1_2)
            angle_diff = abs(angle1 - angle2)
            if -np.pi/36 <= angle_diff <= np.pi/36:
                similar_lines.append(line)
        if similar_lines:
            # 合并相似的线，可以取平均等方式
            merged_line = np.mean(similar_lines, axis=0).astype(np.int32)[0]
            merged_lines.append(merged_line)
    return np.array(merged_lines)



def find_parallel_and_vertical_lines(lines, image):
    parallel_lines = []
    vertical_lines = []
    height, width = image.shape[:2]
    short_edge_length = min(height, width)
    distance_threshold = short_edge_length / 5

    for i, line1 in enumerate(lines):
        x1_1, y1_1, x2_1, y2_1 = line1
        for j in range(i + 1, len(lines)):
            line2 = lines[j]
            x1_2, y1_2, x2_2, y2_2 = line2
            # 计算角度
            angle1 = np.arctan2(y2_1 - y1_1, x2_1 - x1_1)
            angle2 = np.arctan2(y2_2 - y1_2, x2_2 - x1_2)
            angle_diff = abs(angle1 - angle2)
            if (np.pi/2 - angle_diff < np.pi/18) or (angle_diff < np.pi/18):
                # 计算距离
                if angle_diff < np.pi/18:
                    dist = np.max([abs(x1_1 - x1_2), abs(x2_1 - x2_2), abs(y1_1 - y1_2), abs(y2_1 - y2_2)])
                    if dist > distance_threshold:
                        parallel_lines.append((line1, line2))
                else:
                    dist = np.max([abs(x1_1 - x1_2), abs(x2_1 - x2_2), abs(y1_1 - y1_2), abs(y2_1 - y2_2)])
                    if dist > distance_threshold:
                        vertical_lines.append((line1, line2))
    return parallel_lines, vertical_lines



def hough_line_with_path(fpath: str='/Users/samguo/Downloads/blood_pressure_127.png'):

    local_file = Path(fpath)
    content = local_file.read_bytes()
    bytesio = io.BytesIO(content)
    pil_image = Image.open(bytesio)
    np_image = pil_image_to_cv2_image(pil_image)
    # lines = hough_line_with_bytesio(np_image)
    gray = image_to_gray_image(np_image)
    edges = canny_edges_of_image(gray, 50, 150)
    # lines = cv2.HoughLines(edges, 1, np.pi / 180, 100)
    # print(f'lines.count = {len(lines)}')

    # dense_lines = filter_dense_lines(np_image, lines, 50)
    # print(f'dense_lines.count = {len(dense_lines)}')

    # if dense_lines is not None:
    #     for line in dense_lines:
    #         rho, theta = line[0]
    #         a = np.cos(theta)
    #         b = np.sin(theta)
    #         x0 = a * rho
    #         y0 = b * rho
    #         x1 = int(x0 + 1000 * (-b))
    #         y1 = int(y0 + 1000 * (a))
    #         x2 = int(x0 - 1000 * (-b))
    #         y2 = int(y0 - 1000 * (a))
    #         cv2.line(np_image, (x1, y1), (x2, y2), (0, 0, 255), 2)





    # filtered_lines = filter_hough_lines(lines)
    # print(f'lines.count = {len(filtered_lines)}')
    # if filtered_lines is not None:
    #     for rho, theta in filtered_lines:
    #         a = np.cos(theta)
    #         b = np.sin(theta)
    #         x0 = a * rho
    #         y0 = b * rho
    #         x1 = int(x0 + 1000 * (-b))
    #         y1 = int(y0 + 1000 * (a))
    #         x2 = int(x0 - 1000 * (-b))
    #         y2 = int(y0 - 1000 * (a))
    #         cv2.line(np_image, (x1, y1), (x2, y2), (0, 0, 255), 2)

    height, width = np_image.shape[:2]
    short_edge_length = min(height, width)
    # distance_threshold = short_edge_length * .2
    distance_threshold = 50
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=distance_threshold, maxLineGap=20)
    lines = merge_similar_lines(lines)
    print(f'lines.count = {len(lines)}')
    for line in merged_lines:
        x1, y1, x2, y2 = line
        cv2.line(np_image, (x1, y1), (x2, y2), (0, 255, 0), 2)



    cv2.imshow('Hough Lines', np_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# def hough_line_clustering(fpath: str='/Users/samguo/Downloads/blood_pressure_127.png', n_clusters: int=3):

#     local_file = Path(fpath)
#     content = local_file.read_bytes()
#     bytesio = io.BytesIO(content)
#     pil_image = Image.open(bytesio)
#     np_image = pil_image_to_cv2_image(pil_image)

#     gray = image_to_gray_image(np_image)
#     edges = canny_edges_of_image(gray, 50, 100)
#     lines = cv2.HoughLines(edges, 1, np.pi / 180, 100)

#     # 提取直线特征
#     line_features = []
#     index1 = 0
#     for line in lines:
#         print(f'index1 = {index1}')
#         rho, theta = line[0]
#         line_features.append([rho, theta])
#         index1 += 1

#     # 转换为 numpy 数组
#     X = np.array(line_features)

#     # 使用 K-Means 聚类
#     kmeans = KMeans(n_clusters=n_clusters).fit(X)

#     # 聚类结果
#     clusters = {}
#     for i, label in enumerate(kmeans.labels_):
#         print(f'i = {i}')
#         if label not in clusters:
#             clusters[label] = []
#         clusters[label].append(lines[i])

#     # return clusters
#     index2 = 0
#     for cluster_label, lines_in_cluster in clusters.items():
#         # print(f"Cluster {cluster_label}:")
#         for line in lines_in_cluster:
#             print(f'index = {index2}')
#             rho, theta = line[0]
#             # print(f"  rho: {rho}, theta: {theta}")
#             a = np.cos(theta)
#             b = np.sin(theta)
#             x0 = a * rho
#             y0 = b * rho
#             x1 = int(x0 + 1000 * (-b))
#             y1 = int(y0 + 1000 * (a))
#             x2 = int(x0 - 1000 * (-b))
#             y2 = int(y0 - 1000 * (a))
#             cv2.line(np_image, (x1, y1), (x2, y2), (0, 0, 255), 2)
#             index2 += 1

#     cv2.imshow('Hough Lines', np_image)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()





def color_ract_of_image(fpath: str='/Users/samguo/Downloads/blood_pressure_127.png'):
    
    local_file = Path(fpath)
    content = local_file.read_bytes()
    bytesio = io.BytesIO(content)
    pil_image = Image.open(bytesio)
    np_image = pil_image_to_cv2_image(pil_image)
    hsv_image = cv2.cvtColor(np_image, cv2.COLOR_BGR2HSV)
    
    # 保存过滤后的轮廓
    selected_contours = []

    height, width = np_image.shape[:2]
    long_edge_image = max(width, height)
    short_edge_image = min(width, height)

    # 定义颜色范围
    red_lower = np.array([0, 100, 100])
    red_upper = np.array([10, 255, 255])
    red_lower2 = np.array([165, 90, 90])
    red_upper2 = np.array([180, 255, 255])
    orange_lower = np.array([11, 100, 100])
    orange_upper = np.array([25, 255, 255])
    green_lower = np.array([40, 100, 100])
    green_upper = np.array([80, 255, 255])
    gray_lower = np.array([0, 0, 100])
    gray_upper = np.array([180, 100, 200])
    blue_lower = np.array([95, 30, 150])
    blue_upper = np.array([115, 70, 255])
    blue_lower2 = np.array([65, 5, 150])
    blue_upper2 = np.array([100, 35, 255])
    dark_lower = np.array([5, 40, 20])
    dark_upper = np.array([36, 80, 90])

    gray_lower2 = np.array([35, 25, 20])
    gray_upper2 = np.array([80, 120, 110])

    light1_lower = np.array([0, 0, 0])
    light1_upper = np.array([180, 255, 50])
    light2_lower = np.array([0, 0, 0])
    light2_upper = np.array([180, 255, 100])
    light3_lower = np.array([0, 0, 100])
    light3_upper = np.array([180, 255, 200])
    light4_lower = np.array([0, 0, 200])
    light4_upper = np.array([180, 255, 255])

    saturation_zero = np.array([0, 0, 0])
    saturation_lower = np.array([0, 0, 50])
    saturation_lower2 = np.array([0, 0, 155])
    saturation_upper = np.array([0, 0, 255])

    hue_zero = np.array([0, 0, 0])
    hue_lower = np.array([0, 0, 50])
    hue_lower2 = np.array([0, 0, 155])
    hue_upper = np.array([0, 0, 255])
    
    # 天蓝色
    # [104  42 239]
    # [101  58 206]
    # [104  67 176]
    # [105  37 248]
    # [102  60 221]

    # [102  65 196]

    # 更浅的蓝色
    # [ 70  16 232]
    # [ 93  26 185]
    # [ 79  22 239]
    # [ 87  27 179]
    # [ 84  28 183]

    # 深灰色
    # [17 57 72]
    # [17 52 44]
    # [24 51 75]
    # [ 9 51 35]
    # [27 53 86]
    # [27 69 70]
    # [27 47 60]

    # 灰色泛蓝
    # [47 82 28]
    # [72 90 37]
    # [ 58  32 104]
    # [ 78 109 103]


    # 灰色
    # [ 80  13 122]
    # [ 75   4 118]
    # [ 53  14 149]
    # [ 56  15 138]

    # [ 76  16 175]

    # [30 52 84]
    # [25 77 83]


    # color_ranges = [(red_lower, red_upper, 'red'), 
    #                 (red_lower2, red_upper2, 'red2'),
    #                 (orange_lower, orange_upper, 'orange'), 
    #                 (green_lower, green_upper, 'green'), 
    #                 (gray_lower, gray_upper, 'gray'),
    #                 (gray_lower2, gray_upper2, 'gray2'),
    #                 (blue_lower, blue_upper, 'blue'),
    #                 (blue_lower2, blue_upper2, 'blue2'),
    #                 (dark_lower, dark_upper, 'dark'),
    #                 ]

    color_ranges = [
                    (red_lower, red_upper, 'red'), 
                    (red_lower2, red_upper2, 'red2'),
                    (orange_lower, orange_upper, 'orange'), 
                    (green_lower, green_upper, 'green'), 
                    (gray_lower, gray_upper, 'gray'),
                    (gray_lower2, gray_upper2, 'gray2'),
                    (blue_lower, blue_upper, 'blue'),
                    (blue_lower2, blue_upper2, 'blue2'),
                    (dark_lower, dark_upper, 'dark'),
                    (light1_lower, light1_upper, 'light1'),
                    # (light2_lower, light2_upper, 'light2'),
                    # (light3_lower, light3_upper, 'light3'),
                    (light4_lower, light4_upper, 'light4'),
                    (saturation_zero, saturation_lower, 'low_saturation'),
                    (saturation_lower2, saturation_upper, 'hight_saturation'),
                    (hue_zero, hue_lower, 'low_hue'),
                    (hue_lower2, hue_upper, 'hight_hue'),
                    ]

    
    screen_contour = {}

    for lower, upper, color_name in color_ranges:
        mask = cv2.inRange(hsv_image, lower, upper)
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        print(f'contours.count = {len(contours)}, color = {color_name}')
        # epsilon = 0.05 * cv2.arcLength(contours, True)
        # approx_polygon = cv2.approxPolyDP(contours, epsilon, True)

        # l = []
        new_contours = []
        for i, cnt in enumerate(contours):
            parent_idx = hierarchy[0][i][3]
            # if parent_idx!= -1:
            #     # 当前轮廓有父轮廓，可以进一步分析其在层次结构中的位置
            #     # l.insert(0,i)
            #     print(f"特定颜色轮廓 {i} 有父轮廓")
            # else:
            #     # 当前轮廓没有父轮廓，可能是最外层的特定颜色轮廓
            #     print(f"特定颜色轮廓 {i} 是独立的轮廓")
            #     new_contours.append(cnt)
            if parent_idx == -1:
                # print(f"{color_name}轮廓 {i} 是独立的轮廓")
                new_contours.append(cnt)
        
        
        # 寻找到所有无父轮廓的轮廓中面积最大的那个
        if len(new_contours) > 0:
            print(f'new_contours.length = {len(new_contours)}')
            screen_contour[color_name] = {
                'contours': max(new_contours, key=cv2.contourArea),
                # 'approx': approx_polygon
            }
        


    print(f'screen_contour = {len(screen_contour.keys())}')

    if screen_contour is not None:
        keys = screen_contour.keys()
        for key in keys:
            # if key == 'gray':
            #     color = (128, 128, 128) # 灰色
            # elif key == 'gray':
            #     color = (128, 128, 128) # 灰色
            # elif key == 'red':
            #     color = (0, 0, 255) # 红色
            # elif key == 'red2':
            #     color = (0, 255, 255) # 黄色
            # elif key == 'orange':
            #     color = (0, 165, 255) # 橙色
            # elif key == 'green':
            #     color = (0, 255, 0) # 绿色
            # elif key == 'blue':
            #     # break
            #     color = (255, 0, 0) # 蓝色
            # elif key == 'blue2':
            #     # break
            #     color = (255, 255, 0) # 天蓝色
            # elif key == 'dark':
            #     # break
            #     color = (255, 0, 255) # 紫色
            # elif key == 'low_light':
            #     color = (255, 255, 255)
            # elif key == 'hight_light':
            #     color = (255, 255, 0) # 紫色
            # elif key == 'low_saturation':
            #     color = (0, 255, 0) # 紫色
            # elif key == 'hight_saturation':
            #     color = (255, 0, 255) # 紫色
            # elif key == 'low_hue':
            #     color = (255, 0, 0)
            # elif key == 'hight_hue':
            #     color = (0, 255, 255)
            # else:
            #     # break
            #     color = (255, 255, 255)
            
            
            contours = screen_contour[key]['contours']

            area = cv2.contourArea(contours)
            rect = cv2.minAreaRect(contours)


            # '''
            # 过滤掉面积过小的轮廓
            # '''
            # if area < height * width * 0.1:
            #     continue

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
                'contours': contours
            })
            print(f'rect = {rect}')

            # 原始代码，与上方''' ''' 包围的互斥
            # points = cv2.boxPoints(rect)
            # points = np.int0(points)
            # area_rect = rect[1][0] * rect[1][1]
            # if area_rect > 0:
            #     if area / area_rect >= 0.8:
            #         cv2.drawContours(np_image, [contours], -1, color, 2) # (0, 255, 0)
            #         cv2.polylines(np_image, [points], -1, (0,0,255), 3)
            #         # cv2.drawContours(np_image, [screen_contour[key]['approx']], -1, (255, 0, 0), 2) # (0, 255, 0)
            #         print(f"识别到的颜色为：{key}，对应的区域已在图像中标记。")
            #         print(f'points = {points}, area_rect = {area_rect}, area = {area}')
            # 原始代码，与上方''' ''' 包围的互斥
            
            # cv2.drawContours(np_image, [contours], -1, color, 2)
            # cv2.polylines(np_image, [points], -1, (0,0,255), 3)
    
    if len(selected_contours) == 0:
        return

    print(f'selected_contours = {len(selected_contours)}')
    max_area = 0
    largest_rectangle = None
    for item in selected_contours:
        rect = item['rect']
        area = rect[1][0] * rect[1][1]
        if area > max_area:
            max_area = area
            largest_rectangle = item
        
        # points = cv2.boxPoints(item['rect'])
        # points = np.int0(points)
        # cv2.drawContours(np_image, [item['contours']], -1, (255, 0, 255), 2)
        # cv2.polylines(np_image, [points], -1, (0,0,255), 3)

    points = cv2.boxPoints(largest_rectangle['rect'])
    points = np.int0(points)
    print(f'points = {points}')
    cv2.drawContours(np_image, [largest_rectangle['contours']], -1, (255, 0, 255), 2)
    cv2.polylines(np_image, [points], -1, (0,0,255), 3)

    # 显示结果图像
    cv2.imshow('Blood Pressure Screen', np_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def edges_ract_of_image(fpath: str='/Users/samguo/Downloads/blood_pressure_127.png'):
    
    local_file = Path(fpath)
    content = local_file.read_bytes()
    bytesio = io.BytesIO(content)
    pil_image = Image.open(bytesio)
    np_image = pil_image_to_cv2_image(pil_image)
    # hsv_image = cv2.cvtColor(np_image, cv2.COLOR_BGR2HSV)
    gray = image_to_gray_image(np_image)
    edges = canny_edges_of_image(gray, 50, 100)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < 100:  # 过滤掉面积过小的轮廓
            continue
        perimeter = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.04 * perimeter, True)
        if len(approx) == 4:
            # 检查四边形的角度和边长
            rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rect)
            angles = []
            side_lengths = []
            for i in range(4):
                p1 = np.array(box[i])
                p2 = np.array(box[(i + 1) % 4])
                p3 = np.array(box[(i + 2) % 4])
                v1 = p2 - p1
                v2 = p3 - p2
                angle = np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))
                angles.append(angle)
                side_lengths.append(np.linalg.norm(p2 - p1))
            # 可以根据角度和边长的条件进一步确认矩形
            if all(np.isclose(angles[i], np.pi / 2, atol=0.1) for i in range(4)) and np.allclose(side_lengths[0], side_lengths[2], atol=10) and np.allclose(side_lengths[1], side_lengths[3], atol=10):
                cv2.drawContours(edges, [cnt], -1, 255, 2)

    # 显示结果
    cv2.imshow('Approximate Rectangles', edges)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



def gray_ract_of_image(fpath: str='/Users/samguo/Downloads/blood_pressure_127.png'):
    
    local_file = Path(fpath)
    content = local_file.read_bytes()
    bytesio = io.BytesIO(content)
    pil_image = Image.open(bytesio)
    np_image = pil_image_to_cv2_image(pil_image)
    # hsv_image = cv2.cvtColor(np_image, cv2.COLOR_BGR2HSV)
    gray = image_to_gray_image(np_image)
    # hsv_image = cv2.cvtColor(gray, cv2.COLOR_BGR2HSV)
    # hsv_image = gray
# 二值化处理
    ret, binary_image = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        # 定义颜色范围
    # red_lower = np.array([0, 100, 100])
    # red_upper = np.array([10, 255, 255])
    # orange_lower = np.array([11, 100, 100])
    # orange_upper = np.array([25, 255, 255])
    # green_lower = np.array([40, 100, 100])
    # green_upper = np.array([80, 255, 255])
    gray_lower = np.array([0, 0, 100])
    gray_upper = np.array([180, 100, 200])

    # color_ranges = [(red_lower, red_upper, 'red'), 
                    # (orange_lower, orange_upper, 'orange'), 
                    # (green_lower, green_upper, 'green'), 
                    # (gray_lower, gray_upper, 'gray')]
    
    # mask = cv2.inRange(hsv_image, gray_lower, gray_upper)
    # edges = canny_edges_of_image(gray, 50, 100)
    contours, _ = cv2.findContours(binary_image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    print(f'contours = {len(contours)}')

    for cnt in contours:
        # area = cv2.contourArea(cnt)
        # if area < 100:  # 过滤掉面积过小的轮廓
        #     continue
        # perimeter = cv2.arcLength(cnt, True)
        # approx = cv2.approxPolyDP(cnt, 0.04 * perimeter, True)
        # if len(approx) == 4:
        #     # 检查四边形的角度和边长
        #     rect = cv2.minAreaRect(cnt)
        #     box = cv2.boxPoints(rect)
        #     angles = []
        #     side_lengths = []
        #     for i in range(4):
        #         p1 = np.array(box[i])
        #         p2 = np.array(box[(i + 1) % 4])
        #         p3 = np.array(box[(i + 2) % 4])
        #         v1 = p2 - p1
        #         v2 = p3 - p2
        #         angle = np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))
        #         angles.append(angle)
        #         side_lengths.append(np.linalg.norm(p2 - p1))
        #     # 可以根据角度和边长的条件进一步确认矩形
        #     if all(np.isclose(angles[i], np.pi / 2, atol=0.1) for i in range(4)) and np.allclose(side_lengths[0], side_lengths[2], atol=10) and np.allclose(side_lengths[1], side_lengths[3], atol=10):
        cv2.drawContours(gray, [cnt], -1, (255, 255, 255), 2)

    # 显示结果
    cv2.imshow('Approximate Rectangles', gray)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



def mask_of_image(fpath: str='/Users/samguo/Downloads/blood_pressure_127.png'):

    image = cv2.imread(fpath)
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 定义亮度范围
    lower_brightness = np.array([0, 0, 80])  # 例如，亮度大于 50
    upper_brightness = np.array([50, 100, 140])

    mask = cv2.inRange(hsv_image, lower_brightness, upper_brightness)

    # 定义饱和度范围
    # lower_saturation = np.array([0, 0, 0])  # 例如，饱和度大于 50
    # upper_saturation = np.array([180, 50, 255])
    # mask = cv2.inRange(hsv_image, lower_saturation, upper_saturation)

    # 使用掩码提取满足亮度范围的部分
    result = cv2.bitwise_and(image, image, mask=mask)

    # 显示结果
    # cv2.imshow('Original Image', image)
    cv2.imshow('Result', mask)
    # cv2.imshow('merged image', result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



def k_means_bgr_mask_of_image(fpath: str='/Users/samguo/Downloads/blood_pressure_127.png'):
       # 读取图像
   image = cv2.imread(fpath)

   # 将图像转换为一维数组
   pixels = image.reshape((-1, 3))
   pixels = np.float32(pixels)

   # 定义 K-Means 参数
   criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
   k = 5  # 聚类数量，可以根据需要调整

   # 应用 K-Means 聚类
   _, labels, centers = cv2.kmeans(pixels, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

   # 将像素值转换回整数
   centers = np.uint8(centers)

   # 根据聚类标签重新分配像素值
   segmented_image = centers[labels.flatten()]
   segmented_image = segmented_image.reshape(image.shape)

   cv2.imshow('Original Image', image)
   cv2.imshow('Segmented Image', segmented_image)
   cv2.waitKey(0)
   cv2.destroyAllWindows()



def bgr_mask_of_image(fpath: str='/Users/samguo/Downloads/blood_pressure_127.png'):
   # 读取图像
   image = cv2.imread(fpath)

   # 定义目标颜色的 BGR 范围（例如，蓝色）20,21,15   110,130,115, 92,92,90
   lower_blue = np.array([21, 15, 20])
   upper_blue = np.array([110, 130, 115])

   # 创建掩码
   mask = cv2.inRange(image, lower_blue, upper_blue)

   # 使用掩码提取目标颜色区域
   segmented_image = cv2.bitwise_and(image, image, mask=mask)

   cv2.imshow('Original Image', image)
   cv2.imshow('Segmented Image', segmented_image)
   cv2.waitKey(0)
   cv2.destroyAllWindows()



# 对图片进行拉普拉斯锐化
# image: hsv格式的图片
# return: 合并后的hsv格式图片
def laplacian_image(image):

    h, s, v = cv2.split(image)
    # 定义拉普拉斯算子
    laplacian_kernel = np.array([[0, -1, 0],
                                [-1, 5, -1],
                                [0, -1, 0]])
    # 对亮度通道进行拉普拉斯锐化
    sharpened_v = cv2.filter2D(v, -1, laplacian_kernel)
    # 合并处理后的通道
    sharpened_hsv = cv2.merge((h, s, sharpened_v))
    # 转换回 BGR 颜色空间
    sharpened_image = cv2.cvtColor(sharpened_hsv, cv2.COLOR_HSV2BGR)
    return sharpened_image


# 对灰度图片进行拉普拉斯锐化
# image: 灰度图片
# return: 灰度锐化后的通道
def laplacian_for_gray_image(image):

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    

# def rect_of_image(image):

#     color_ranges = [
#                     (red_lower, red_upper, 'red'), 
#                     (red_lower2, red_upper2, 'red2'),
#                     (orange_lower, orange_upper, 'orange'), 
#                     (green_lower, green_upper, 'green'), 
#                     (gray_lower, gray_upper, 'gray'),
#                     (gray_lower2, gray_upper2, 'gray2'),
#                     (blue_lower, blue_upper, 'blue'),
#                     (blue_lower2, blue_upper2, 'blue2'),
#                     (dark_lower, dark_upper, 'dark'),
#                     (light_zero, light_lower, 'low_light'),
#                     (light_lower2, light_upper, 'hight_light'),
#                     (saturation_zero, saturation_lower, 'low_saturation'),
#                     (saturation_lower2, saturation_upper, 'hight_saturation'),
#                     (hue_zero, hue_lower, 'low_hue'),
#                     (hue_lower2, hue_upper, 'hight_hue'),
#                     ]


def laplacian_mask_of_image(fpath: str='/Users/samguo/Downloads/blood_pressure_127.png'):
    image = cv2.imread(fpath)
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    sharpened_image = laplacian_image(hsv_image)

    # 显示原始图像和锐化后的图像
    # cv2.imshow('Original Image', image)
    cv2.imshow('Sharpened Image', sharpened_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        # hough_line_with_path(sys.argv[1])
        # hough_line_clustering(sys.argv[1])
        # color_ract_of_image(sys.argv[1])
        mask_of_image(sys.argv[1])
        # edges_ract_of_image(sys.argv[1])
        # gray_ract_of_image(sys.argv[1])
        # bgr_mask_of_image(sys.argv[1])
        # laplacian_mask_of_image(sys.argv[1])
    else:
        # hough_line_with_path()
        # hough_line_clustering()
        # color_ract_of_image()
        mask_of_image()
        # edges_ract_of_image()
        # gray_ract_of_image()
        # bgr_mask_of_image()
        # laplacian_mask_of_image()
