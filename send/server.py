import os
import sys

import yaml
import json
from flask import Flask, jsonify, request
import requests
import utils

app = Flask(__name__)


@app.route('/ready', methods=['GET'])
def ready():
    # 这里就要开始进行文件的压缩，分片,l
    args = request.get_json()
    file_name = args['file_name']
    conf = utils.config()
    source_dir = os.path.join(conf['source_dir'], file_name)
    if not os.path.exists(source_dir):
        return jsonify({'code': -1, 'msg': f'{file_name} 不存在', 'res': {}})

    try:
        # 压缩文件  以及分片处理
        utils.compress_folder(file_name,conf)
        return jsonify({'code': 0, 'msg': 'ready success', 'res': {}})
    except Exception as e:
        print(e)
        return jsonify({'code': -1, 'msg': 'ready fail', 'res': {}})


# 发送文件：所有文件，包括当前文件和总的文件
@app.route('/send', methods=['GET'])
def send():
    args = request.get_json()
    file_name = f"{args['file_name']}"
    current_id = args['last'] + 1
    total = utils.get_chunk_number(file_name)

    conf = utils.config()
    file_path = os.path.join(conf['zip_split_dir'], file_name, '')
    file_path = f"{file_path}_{current_id}.zip"
    print(file_path)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/76.0.3809.100 Safari/537.36',

        'Content-Type': 'application/json'
    }
    params = {
        'current_id': current_id,
        'total': total
    }
    files = {'file': open(file_path, 'rb')}
    print(conf)
    url = f'http://{conf["remote"]}/upload'
    print(url)
    response = requests.post(url=url, data=params, files=files)
    print(response.text)
    return jsonify({'code': 0, 'msg': 'success', 'res': {}})


@app.route('/maps', methods=['GET'])
def mapping():
    conf = utils.config()
    source_dir = os.path.join(conf["source_dir"])
    maps = utils.scan2(source_dir)
    return jsonify({'code': 0, 'msg': '', 'res': maps})


@app.route('/done', methods=['GET'])
def done():
    a = {}
    # 这里即完成一个压缩文件的传输


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999, debug=True)

res = utils.get_chunk_number('20231012')
