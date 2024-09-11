import os
import json
import sys

from pathlib import Path



def get_rect_from_path(file_path: str) -> float:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if 'output' in data and isinstance(data['output'], dict):
                if 'rect' in data['output']:
                    return data['output']['rect']
            return None
    except FileNotFoundError:
        return None
    except json.jsonDecodeError:
        return None
    


def find_correct_rect(file_path: str) -> float:

    rect = get_rect_from_path(file_path)
    return rect


def is_json(file_path):
    extension = os.path.splitext(file_path)[1].lower()
    return extension in ['.json']



def testit(file_path=None):

    with open('b.txt', 'a', encoding='utf-8') as file:

        file.write("'''")

        if file_path is None:
            print("没有提供文件路径参数，使用默认路径。")
            file_path = '/Users/samguo/Workspace/resources/result_sugar'

        json_names = os.listdir(file_path)

        for json_name in json_names:
            print(f'json_name = {json_name}')
            full_path = os.path.join(file_path, json_name)
            if is_json(full_path) == False:
                continue
            rect = get_rect_from_path(full_path)

            min_x = round(rect[0][0] - 5 if rect[0][0] - 5 > 0 else 0, 2)
            max_x = round((rect[0][0] + 5), 2)

            min_y = round(rect[0][1] - 5 if rect[0][1] - 5 > 0 else 0, 2)
            max_y = round((rect[0][1] + 5), 2)
            
            min_width = round(rect[1][0] - 5 if rect[1][0] - 5 > 0 else 0, 2)
            max_width = round((rect[1][0] + 5), 2)

            min_height = round(rect[1][1] - 5 if rect[1][1] - 5 > 0 else 0, 2)
            max_height = round((rect[1][1] + 5), 2)

            min = ((min_x, min_y), (min_width, min_height))
            max = ((max_x, max_y), (max_width, max_height))

            txt = '>>> is_between(find_correct_rect(\''+full_path+'\'), ' + f'{min},' + f'{max})'

            file.write('\n' + txt)
            file.write('\n' + 'True')
            # '''
            # >>> is_between(find_correct_angle('v:/test.png'), -5,5)
            # True
            # '''

            # file.write('\n' + 'aaaaaa')
        file.write('\n' + "'''")




if __name__ == '__main__':
    if len(sys.argv) > 1:
        # color_ract_of_image(sys.argv[1])
        testit(sys.argv[1])
        # testit_with_filed_files(sys.argv[1])
    else:
        # color_ract_of_image()
        testit()
        # testit_with_filed_files()