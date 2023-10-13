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


def has_lock() -> bool:
    return os.path.exists('.lock')


def create_lock(file_name: str):
    if not os.path.exists(file_name):
        with open(file_name, 'w') as lock_file:
            lock_file.write(os.path.basename(file_name))


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
