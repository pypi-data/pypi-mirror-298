import os


def read_properties(file_path):
    properties = {}

    # 检查文件是否存在
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                # 跳过空行和注释行
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    properties[key.strip()] = value.strip()

    return properties
