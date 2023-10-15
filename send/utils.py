import os
import sys
import zipfile
import requests

import yaml


def compress_folder(file_name,conf):
    folder_path = os.path.join(conf['source_dir'], file_name)
    save_path = os.path.join(conf['zip_compress_dir'])
    save_name = f'{file_name}.zip'
    zip_filename = os.path.join(save_path, save_name)

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
    output_prefix = os.path.join(conf['zip_split_dir'], file_name,'')
    split_zip_with_structure(zip_filename, output_prefix, 10)

def add_dir_split(input_zip, output_prefix):
    file_name, file_extension = os.path.splitext(os.path.basename(input_zip))
    output_prefix = os.path.join(output_prefix, file_name)
    output_prefix = os.path.join(output_prefix, '')
    return output_prefix


def split_zip_with_structure(input_zip, output_prefix, chunk_size):

    if not os.path.exists(output_prefix):
        os.mkdir(output_prefix)

    with zipfile.ZipFile(input_zip, 'r') as zip_file:
        file_list = zip_file.namelist()
        chunk_num = 1
        while file_list:
            chunk_files = file_list[:chunk_size]
            with zipfile.ZipFile(f'{output_prefix}_{chunk_num}.zip', 'w') as chunk_zip:
                for file in chunk_files:
                    with zip_file.open(file) as original_file:
                        chunk_zip.writestr(file, original_file.read())
            file_list = file_list[chunk_size:]
            chunk_num += 1


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

# 先做再优化把

# 更优雅的分片解决方案: 是文件夹则不分片，不是文件夹的时候才进行分片

# 需要解决的一个大的难题是，如果一个子文件夹里面的某个文件非常应该怎么处理呢？

# 嗯我的想法是将这个大文件进行分片，但是不和其他文件合在一起。
