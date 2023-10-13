import json

from flask import Flask, render_template, request, jsonify
import yaml
import requests
from werkzeug.utils import secure_filename
import os
import utils

app = Flask(__name__)
config = utils.conf()

# 还是我主动来拉去文件吧
# 发送方接口： 返回顶层的目录文件列表；  提供 发送分片 的接口以及总共的分片个数和当前位置的接口； 是否完全接收完成的接口；
# 其中就包括了文件压缩；分片；分片完成之后，（对比压缩文件和总分片，确认无误之后在删除源文件）；完成之后删除分片。。。


# 接收放接口：好像没有要对外暴露的接口
@app.route('/', methods=['GET'])
def index():
    # res = requests.post()
    print(1)


@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # 获取 JSON 数据
        print(123123123)
        # 获取文件数据
        # if 'file' in request.files:

        file = request.files['file']
        filename = secure_filename(file.filename)
        save = os.path.join(config['chunk_save_dir'], filename)
        print(f"save path = {save}")
        file.save(save)
        print("Received file:", filename)

        return jsonify({'code': '0', 'message': 'success'})
    else:
        return jsonify({'code': '0', 'message': 'not POST request'})


def main():
    with open("config.yaml", "r") as config_file:
        return yaml.load(config_file, Loader=yaml.FullLoader)


if __name__ == '__main__':
    app.run("0.0.0.0", port=7777, debug=True)