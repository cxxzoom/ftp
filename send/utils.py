import concurrent
import shutil
from concurrent import futures
import os
import sys
import threading
import zipfile
from datetime import datetime

import requests
import yaml
from flask import jsonify


def compress_folder(file_name, conf):
    folder_path = os.path.join(conf['source_dir'], file_name)
    save_path = os.path.join(conf['zip_compress_dir'])
    zip_filename = os.path.join(save_path, f'{file_name}.zip')

    if not os.path.exists(save_path):
        os.mkdir(save_path)
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, folder_path))

    # 分片处理
    if not os.path.exists(conf['zip_split_dir']):
        os.mkdir(conf['zip_split_dir'])
    output_prefix = os.path.join(conf['zip_split_dir'], file_name, '')
    split_zip_with_structure(zip_filename, output_prefix, conf['chunk_size'])


def split_zip_with_structure(input_zip, output_prefix, chunk_size):
    if not os.path.exists(output_prefix):
        os.mkdir(output_prefix)
    destination = os.path.join(output_prefix, '', '1.zip')
    # print(input_zip, destination)
    # 这里就是不分片，直接cv过去
    # shutil.move(input_zip, destination)

    with zipfile.ZipFile(input_zip, 'r') as zip_file:
        file_list = zip_file.namelist()
        tmp_size = min(len(file_list), chunk_size)
        chunk_num = 1
        while file_list:
            chunk_files = file_list[:tmp_size]
            with zipfile.ZipFile(f'{output_prefix}{chunk_num}.zip', 'w') as chunk_zip:
                for file in chunk_files:
                    with zip_file.open(file) as original_file:
                        chunk_zip.writestr(file, original_file.read())
            file_list = file_list[tmp_size:]
            chunk_num += 1

    # 分片完成之后删除源文件
    os.remove(input_zip)


def scan(path, my_dir: dict, base_path: str, i):
    files = os.listdir(path)

    for file in files:
        tmp = os.path.join(path, file)
        if os.path.isfile(tmp):
            name = tmp[len(base_path):]
            i = i + 1
            my_dir[i] = name
            print(my_dir)
        if os.path.isdir(tmp):
            scan(tmp, my_dir, base_path, i)


def config() -> dict:
    with open('config.yaml', 'r') as yaml_config:
        c = yaml.load(yaml_config, Loader=yaml.FullLoader)
        return c


def get_chunk_number(file_name: str) -> int:
    conf = config()
    files = os.listdir(os.path.join(conf['zip_split_dir'], file_name))
    return len(files)


# 获取这个文件下的文件个数
def scan2(path):
    my_dir = {}
    files = os.listdir(path)
    for file in files:
        my_dir[file] = 0
        for root, dirs, files in os.walk(os.path.join(path, file)):
            my_dir[file] += len(files)

    return my_dir


def dd(var):
    print(var)
    sys.exit()


def upload2(file_path, file_name, remote):
    files = {'file': open(file_path, 'rb')}
    url = f'http://{remote}/upload'
    print('in upload ...')
    response = requests.post(url=url, data={'file_name': file_name}, files=files)
    print(response.json(), flush=True)


# 这里写个线程池来管理上传
def thread_upload(file_name):
    conf = config()
    chunk_path = os.path.join(conf['zip_split_dir'], file_name, '')
    print(f'chunk_path:{chunk_path}')
    remote = conf['remote']
    # 遍历这下面的文件总数
    chunks = os.listdir(chunk_path)
    tmp_list = []
    for value in chunks:
        tmp_list.append(os.path.join(chunk_path, value))

    # for file in tmp_list:
    #     threading.Thread(target=upload2, args=(file, file_name, remote)).start()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(upload2, tmp_list,[file_name] * len(tmp_list), [remote] * len(tmp_list))
        for result in results:
            print(result)
