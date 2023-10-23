import os
import shutil
import requests
from flask import Flask, jsonify, request
import utils

app = Flask(__name__)


@app.route('/ready', methods=['GET'])
def ready():
    # 这里就要开始进行文件的压缩，分片,l
    args = request.get_json()
    file_name = args['file_name']

    print(f'{utils.now2()} : 接收到准备文件 : {file_name} 的请求 ...')
    conf = utils.config()
    source_dir = os.path.join(conf['source_dir'], file_name)

    if not os.path.exists(source_dir):
        return jsonify({'code': -1, 'msg': f'{file_name} 不存在', 'res': {}})

    try:
        # 压缩文件  以及分片处理
        # 这里可以起个线程去处理，然后直接返回，然后提供一个确认是否完成的接口，完成了就返回true
        utils.compress_folder(file_name, conf)
        return jsonify({'code': 0, 'msg': 'ready success', 'res': {}})
    except Exception as e:
        print(e)
        return jsonify({'code': -1, 'msg': f'ready fail:{e}', 'res': {}})


# 发送文件：所有文件，包括当前文件和总的文件
@app.route('/send', methods=['POST'])
def send():
    # 参数获取
    args = request.get_json()
    file_name = f"{args['file_name']}"
    current_id = args['last']
    # 通过文件名获取分片数量
    total = utils.get_chunk_number(file_name)
    # 安全控制
    current_id = min(current_id, total)

    conf = utils.config()
    file_path = os.path.join(conf['zip_split_dir'], file_name, '', f"{current_id}.zip")
    files = {'file': open(file_path, 'rb')}
    url = f'http://{conf["remote"]}/upload'
    print(f'{utils.now2()} : 正在传输文件 : {file_name}...')
    response = requests.post(url=url, data={'file_name': file_name}, files=files)
    return jsonify({'code': 0, 'msg': 'success', 'res': {}})


# 现在使用多线程传
@app.route('/send2', methods=['POST'])
def send2():
    # 参数获取
    args = request.get_json()
    file_name = f"{args['file_name']}"
    # 从这里开始就是扫描文件了
    print(f'{utils.now2()} : 正在多线程传输文件 : {file_name}...')

    utils.thread_upload(file_name)
    return jsonify({'code': 0, 'msg': 'tread uploading', 'res': {}})


@app.route('/maps', methods=['GET'])
def mapping():
    print(f'{utils.now2()} : 正在扫描资源文件 :...')
    conf = utils.config()
    source_dir = os.path.join(conf["source_dir"])
    maps = utils.scan2(source_dir)
    return jsonify({'code': 0, 'msg': 'success', 'res': maps})


@app.route('/chunk_count', methods=['GET'])
def chunk_count():
    args = request.get_json()
    file_name = f"{args['file_name']}"
    conf = utils.config()
    print(f'{utils.now2()} : 正在获取资源文件:{file_name} 切片个数...')

    chunk_dir = os.path.join(conf['zip_split_dir'], file_name, '')
    if os.path.exists(chunk_dir):
        files = os.listdir(chunk_dir)
        return jsonify({'code': 0, 'msg': 'success', 'res': {'count': len(files)}})

    return jsonify({'code': -1, 'msg': 'file not exist', 'res': {'count': 0}})


@app.route('/done', methods=['GET'])
def done():
    args = request.get_json()
    file_name = f"{args['file_name']}"
    conf = utils.config()
    zip_path = os.path.join(conf['zip_compress_dir'], file_name + '.zip')
    chunk_dir = os.path.join(conf['zip_split_dir'], file_name, '')
    # 这里即完成一个压缩文件的传输
    if os.path.exists(zip_path):
        os.remove(zip_path)
    if os.path.exists(chunk_dir):
        shutil.rmtree(chunk_dir)

    return jsonify({'code': 0, 'msg': 'success', 'res': {}})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999, debug=False)
