from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import utils
import threading
import main

app = Flask(__name__)
config = utils.conf()


# 提供给远程的文件上传接口
@app.route('/upload', methods=['POST'])
def upload_file():
    print('i was invoked')
    try:
        # 获取 form 数据
        # 获取文件数据
        dir_name = request.form['file_name']
        file = request.files['file']
        filename = secure_filename(file.filename)

        if not os.path.exists(config['chunk_save_dir']):
            os.mkdir(config['chunk_save_dir'])

        chunk_dir = os.path.join(config['chunk_save_dir'], dir_name, '')
        if not os.path.exists(chunk_dir):
            os.mkdir(chunk_dir)

        file.save(os.path.join(chunk_dir, filename))
        print("Received file:", filename)

        return jsonify({'code': '0', 'message': 'success'})
    except Exception as e:
        return jsonify({'code': '-1', 'message': f'bad request with:{e}'})


if __name__ == '__main__':
    threading.Thread(target=main.main).start()
    app.run("0.0.0.0", port=7777, debug=False)
