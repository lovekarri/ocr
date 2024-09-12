import os
import sys
import shutil



PRESSURE_PATH = '/Users/samguo/Workspace/resources/blood_pressure'
SUGAR_PATH = '/Users/samguo/Workspace/resources/blood_sugar'
JSON_PATH = '/Users/samguo/Workspace/python/ocr/test/contours_json/'
NEW_PRESSURE_PATH = '/Users/samguo/Workspace/resources/new_pressure'
NEW_SUGAR_PATH = '/Users/samguo/Workspace/resources/new_sugar'

PRESSURE_JSON = '/Users/samguo/Workspace/resources/result_pressure'
SUGAR_JSON = '/Users/samguo/Workspace/resources/result_sugar'
        
folder_a = PRESSURE_PATH
folder_b = SUGAR_PATH
folder_c = JSON_PATH
folder_d = NEW_PRESSURE_PATH
folder_e = NEW_SUGAR_PATH

folder_f = PRESSURE_JSON
folder_g = SUGAR_JSON

def copy_files(file_path=None):
    # 获取 C 文件夹中的 JSON 文件名列表（不包括扩展名）
    json_files = [os.path.splitext(file)[0] for file in os.listdir(folder_c) if file.endswith('.json')]

    # 遍历 A 文件夹中的图片文件
    for file in os.listdir(folder_a):
        if file.endswith(('.png', '.jpg', '.jpeg')):
            file_name_without_extension = os.path.splitext(file)[0]
            if file_name_without_extension not in json_files:
                shutil.copy(os.path.join(folder_a, file), folder_d)

    # 遍历 B 文件夹中的图片文件
    for file in os.listdir(folder_b):
        if file.endswith(('.png', '.jpg', '.jpeg')):
            file_name_without_extension = os.path.splitext(file)[0]
            if file_name_without_extension not in json_files:
                shutil.copy(os.path.join(folder_b, file), folder_e)


def remove_files(file_path=None):
    # 获取 F 文件夹中的 JSON 文件名列表（不包括扩展名）
    pressure_json_files = [os.path.splitext(file)[0] for file in os.listdir(folder_f) if file.endswith('.json')]

    # 遍历 D 文件夹中的图片文件
    for file in os.listdir(folder_d):
        if file.endswith(('.png', '.jpg', '.jpeg')):
            file_name_without_extension = os.path.splitext(file)[0]
            if file_name_without_extension in pressure_json_files:
                print(file)
                os.remove(os.path.join(folder_d, file))

     # 获取 G 文件夹中的 JSON 文件名列表（不包括扩展名）
    sugar_json_files = [os.path.splitext(file)[0] for file in os.listdir(folder_g) if file.endswith('.json')]

    # 遍历 e 文件夹中的图片文件
    for file in os.listdir(folder_e):
        if file.endswith(('.png', '.jpg', '.jpeg')):
            file_name_without_extension = os.path.splitext(file)[0]
            if file_name_without_extension in sugar_json_files:
                print(file)
                os.remove(os.path.join(folder_e, file))




def copy_json_files(file_path=None):

    for source_folder in [PRESSURE_JSON, SUGAR_JSON]:
        for file_name in os.listdir(source_folder):
            if file_name.endswith('.json'):
                source_path = os.path.join(source_folder, file_name)
                destination_path = os.path.join(JSON_PATH, file_name)
                if not os.path.exists(destination_path):
                    shutil.copy(source_path, JSON_PATH)
                    print(f'{file_name} 已从 {source_folder} 拷贝到 {JSON_PATH}。')
                else:
                    print(f'{file_name} 已存在于 {JSON_PATH}，不进行拷贝。')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        # copy_files(sys.argv[1])
        # remove_files(sys.argv[1])
        copy_json_files(sys.argv[1])
    else:
        # copy_files()
        # remove_files()
        copy_json_files()