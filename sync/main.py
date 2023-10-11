import os
import yaml
from flask import Flask,jsonify

app = Flask(__name__)


@app.route('/')
def mapping():
    dir_ = yaml_config
    
    # mappings = {}
    # scan(dir_,mappings)
    # print("hello world!")
    # return mappings
    return "hello world"



def scan(path, my_dir):
    files = os.listdir(path)

    for file in files:
        tmp = os.path.join(path, file)
        if os.path.isfile(tmp):
            print(tmp)

        if os.path.isdir(tmp):
            print("this is dir->%s", tmp)
            scan(tmp, my_dir)


def yaml_config():
    yaml_file_path = 'config.yaml'

    # 打开YAML文件并解析内容
    with open(yaml_file_path, 'r') as yaml_file:
        yaml_data = yaml.load(yaml_file, Loader=yaml.FullLoader)
    return yaml_data if yaml_data else {}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999)
