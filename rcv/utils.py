import json
import shutil
import zipfile
import os
import requests
import yaml
from flask import logging
from datetime import datetime


# 合并文件
def merge_zips_with_structure(map):
    confs = conf()
    output_zip = os.path.join(confs['chunk_unzip_dir'], map) + '.zip'
    input_prefix = os.path.join(confs['chunk_save_dir'], map, '')
    total_chunks = len(os.listdir(os.path.join(confs['chunk_save_dir'], map)))
    with zipfile.ZipFile(output_zip, 'w') as zip_file:
        for i in range(1, total_chunks + 1):
            with zipfile.ZipFile(f'{input_prefix}{i}.zip', 'r') as chunk_zip:
                for file_info in chunk_zip.infolist():
                    with chunk_zip.open(file_info) as file:
                        zip_file.writestr(file_info.filename, file.read())

    unzip_file(output_zip, os.path.join(confs['chunk_unzip_dir'], map, ''))


# 解压文件
def unzip_file(zip_file, target_dir):
    with zipfile.ZipFile(zip_file, 'r') as zipf:
        zipf.extractall(target_dir)


# 判断是否存在lock文件
def has_lock() -> bool:
    return os.path.exists('.lock')


# 创建正在传输的文件
def create_lock(file_name: str):
    with open('.lock', 'w') as lock_file:
        lock_file.write(os.path.basename(file_name))


def get_lock_file():
    with open('.lock', 'r') as lock_file:
        ctx = lock_file.read()
        return ctx if ctx else ''


def req(params: dict, method='GET', url: str = ''):
    if method == 'GET':
        response = requests.get(params=params, url=url)
    else:
        response = requests.post(params=params, url=url)

    if response.status_code == 200:
        return response
    else:
        # TODO 记录日志
        return response


def conf():
    with open('config.yaml', 'r') as config_file:
        return yaml.load(config_file, Loader=yaml.FullLoader)


# 获取远程需要传输的文件列表
def get_mapping():
    confs = conf()
    response = requests.get(f'http://{confs["remote"]}/maps')
    code, msg, res = response.json()['code'], response.json()['msg'], response.json()['res']
    if code == 0:
        # print(res)
        with open('maps.json', 'w') as file:
            json.dump(res, file)


# 考虑这里是不是需要
# 或者直接每次传输的时候直接去拉去不就得了？
# 获取需要传输的文件列表--本地
def get_maps():
    with open('maps.json', 'r') as file:
        maps = json.load(file)
        return maps if maps else {}


# 从远程拉去chunk文件
def pull_file(params: dict) -> bool:
    confs = conf()
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/76.0.3809.100 Safari/537.36',

        'Content-Type': 'application/json'
    }
    response = requests.post(f'http://{confs["remote"]}/send', json=params, headers=header)
    res = response.text

    print(res)
    # if res['code'] != 0:
    #     return False
    return True


# 判断是否全部传输完成。如果没全部传输完成，则重新
def chunks_finish(file_name):
    confs = conf()
    files = scan2(os.path.join(confs['chunk_unzip_dir'], file_name))

    with open('maps.json', 'r') as file:
        res = json.load(file)
    if res[file_name] == files['count']:
        return True
    return False


# TODO
def get_chunk_number(file_name: str) -> int:
    confs = conf()
    files = os.listdir(os.path.join(conf['zip_split_dir'], file_name))
    with open('maps.json', 'r') as file:
        res = json.load(file)
        num = res[file_name]
    return len(files)


def ready(file_name: str) -> bool:
    confs = conf()
    response = requests.get(f'http://{confs["remote"]}/ready')
    print(f'rcv->ready->{response.text}')
    if response.status_code == 200:
        return True
    return False


# 获取远程当前文件的分片数量
def remote_chunk_count(file_name: str) -> dict:
    confs = conf()
    params = {'file_name': file_name}
    response = requests.get(f'http://{confs["remote"]}/chunk_count', json=params)
    res = response.json()
    return res['res']


# 扫描文件个数
#
def scan2(path):
    my_dir = {}
    files = os.listdir(path)
    my_dir['count'] = 0
    for file in files:
        # 如果是文件的话，不需要扫描，但是要加1
        if os.path.isfile(os.path.join(path, file)):
            my_dir['count'] += 1
        for root, dirs, files in os.walk(os.path.join(path, file)):
            my_dir['count'] += len(files)
    return my_dir


def clean_files(file_name: str):
    confs = conf()
    # 删除chunk文件
    # 删除zip文件
    try:
        # 递归删除chunk文件
        # 删除压缩包
        # 删除.lock真正在执行的任务
        chunk_dir = os.path.join(confs['chunk_save_dir'], file_name, '')
        zip_file = os.path.join(confs['chunk_unzip_dir'], file_name) + '.zip'

        if os.path.exists(chunk_dir):
            shutil.rmtree(chunk_dir)

        if os.path.exists(zip_file):
            os.remove(zip_file)

        with open('.lock', 'w') as f:
            f.write('')

        return True
    except Exception as e:
        return False


# 开始之前创建必要的文件夹以免不必要的错误
def before():
    confs = conf()
    if not os.path.exists(confs['chunk_save_dir']):
        os.mkdir(confs['chunk_save_dir'])

    if not os.path.exists(confs['chunk_unzip_dir']):
        os.mkdir(confs['chunk_unzip_dir'])


def log():
    confs = conf()
    log_dir = os.path.join(confs['log_save_dir'])
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)

    now = datetime.now()
    log_mon = os.path.join(log_dir, now.strftime("%Y%m"), '')
    if not os.path.exists(log_mon):
        os.mkdir(log_mon)
