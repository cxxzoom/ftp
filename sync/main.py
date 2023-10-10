import os
import yaml

def scan(path, my_dir):
    files = os.listdir(path)

    for file in files:
        tmp = os.path.join(path, file)
        if os.path.isfile(tmp):
            print(tmp)

        if os.path.isdir(tmp):
            print("this is dir->%s", tmp)
            scan(tmp, mydir)


def yaml_config():
    yaml_file_path = 'config.yaml'

    # 打开YAML文件并解析内容
    with open(yaml_file_path, 'r') as yaml_file:
        yaml_data = yaml.load(yaml_file, Loader=yaml.FullLoader)

    print(yaml_data)


my_dir = {}
# scan("F:\\script_boy", my_dir)

dire = {}

print(dire)

yaml_config()

