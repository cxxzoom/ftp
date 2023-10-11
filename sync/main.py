import os
import yaml
import json
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/mapping')
def mapping():
    config = {}
    yaml_config(config)

    mappings = {}
    scan(config['config']['local']['dir'], mappings, config['config']['local']['dir'], 0)
    with open('mapping.json', 'w') as f:
        json.dump(mappings, f, indent=4)
    return jsonify(mappings)


# 如果是传的dirs 则返回目录列表和文件个数
# 如果是传的single_dir ,则返回这个文件夹下的所有文件
# 如果是传的single_file,则ftp上传这个文件
@app.route('scan_files', methods=['GET'])
def get_files():
    files = {}
    dirs = request.args.get('dirs') if request.args.get('dirs') else ''
    single_dir = request.args.get('single_dir') if request.args.get('single_dir') else ''



def scan(path, my_dir, basepath, i):
    files = os.listdir(path)

    for file in files:
        tmp = os.path.join(path, file)
        if os.path.isfile(tmp):
            name = tmp[len(basepath):]
            i = i + 1
            my_dir[i] = name
        if os.path.isdir(tmp):
            scan(tmp, my_dir, basepath, i)


def yaml_config(config):
    yaml_file_path = 'config.yaml'

    # 打开YAML文件并解析内容
    with open(yaml_file_path, 'r') as yaml_file:
        config['config'] = yaml.load(yaml_file, Loader=yaml.FullLoader)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999)
