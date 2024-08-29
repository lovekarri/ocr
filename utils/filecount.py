import os

def count_file_types_in_folder(folder_path):
    file_types = {}
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_extension = os.path.splitext(file)[1].lower()
            if file_extension not in file_types:
                file_types[file_extension] = 1
            else:
                file_types[file_extension] += 1
    return file_types


def count_file(folder_path='/paddle'):
    file_type_counts = count_file_types_in_folder(folder_path)

    for file_type, count in file_type_counts.items():
        print(f"文件类型 {file_type} 的数量为：{count}")


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        count_file(sys.argv[1])
    else:
        count_file()