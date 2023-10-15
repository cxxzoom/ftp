import json
import zipfile
import os
import requests
import yaml
from flask import logging


def merge_zips_with_structure(output_zip, input_prefix, total_chunks):
    with zipfile.ZipFile(output_zip, 'w') as zip_file:
        for i in range(1, total_chunks + 1):
            with zipfile.ZipFile(f'{input_prefix}_{i}.zip', 'r') as chunk_zip:
                for file_info in chunk_zip.infolist():
                    with chunk_zip.open(file_info) as file:
                        zip_file.writestr(file_info.filename, file.read())


# 判断是否存在lock文件
def has_lock() -> bool:
    return os.path.exists('.lock')


# 创建正在传输的文件
def create_lock(file_name: str):
    with open(file_name, 'w') as lock_file:
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
    response = requests.post(f'http://{confs["remote"]}/send', json=params,headers=header)
    res = response.text

    print(res)
    # if res['code'] != 0:
    #     return False
    return True


# 判断是否全部传输完成。如果没全部传输完成，则重新
def chunks_finish(file_name):
    confs = conf()

    return {}


# TODO
def get_chunk_number(file_name: str) -> int:
    confs = conf()
    files = os.listdir(os.path.join(conf['zip_split_dir'], file_name))
    with open('maps.json', 'r') as file:
        res = json.load(file)
        num = res[file_name]
    return len(files)
