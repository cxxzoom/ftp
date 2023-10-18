import concurrent
import os
import sys
import threading

import requests
from flask import jsonify
import zipfile

import utils


def scan(path, my_dir, basepath, i):
    files = os.listdir(path)

    for file in files:
        tmp = os.path.join(path, file)
        if os.path.isfile(tmp):
            name = tmp[len(basepath):]
            i = i + 1
            my_dir[i] = name
            print(my_dir)
        if os.path.isdir(tmp):
            scan(tmp, my_dir, basepath, i)


def compress_folder(folder_path, save_path, save_name):
    zip_filename = save_path + save_name
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, folder_path))


# 分割文件
def split_file(input_file, chunk_size, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    with open(input_file, 'rb') as f:
        data = f.read(chunk_size)
        chunk_num = 0
        while data:
            output_file = os.path.join(output_dir, f'chunk_{chunk_num}')
            with open(output_file, 'wb') as chunk_f:
                chunk_f.write(data)
            chunk_num += 1
            data = f.read(chunk_size)


def merge_split_files(split_dir, merged_file):
    with open(merged_file, 'wb') as output_file:
        for root, dirs, files in os.walk(split_dir):
            for file in sorted(files):
                chunk_file = os.path.join(root, file)
                with open(chunk_file, 'rb') as chunk_f:
                    output_file.write(chunk_f.read())


# 解压文件
def unzip_file(zip_file, target_dir):
    with zipfile.ZipFile(zip_file, 'r') as zipf:
        dd(zipf)
        zipf.extractall(target_dir)


def dd(var):
    print(var)
    sys.exit()


# 这里的source_path 是要通过循环来的，所以一次只有一个
source_path = 'F:\\cxxzoom\\ftp\\test_pdf\\20231012'
extension = '.zip'
file_name = os.path.basename(source_path)
save_path = 'F:\\cxxzoom\\ftp\\save\\chunk\\'
save_name = file_name + extension
# compress_folder(source_path, save_path, save_name)
# 分割文件

split_file_path = 'F:\\cxxzoom\\ftp\\public\\chunk\\'


# split_file(save_path + save_name, 1024 * 1024 * 20, split_file_path)

# # 解压和合并应该是在另一个文件夹下
# merge_split_files(split_file_path, 'F:\\cxxzoom\\ftp\\sync\\merge.zip')
# unzip_file('F:\\cxxzoom\\ftp\\sync\\merge.zip', 'F:\\cxxzoom\\ftp\\sync\\merge_', )
def add_dir_split(input_zip, output_prefix):
    file_name, file_extension = os.path.splitext(os.path.basename(input_zip))
    output_prefix = os.path.join(output_prefix, file_name)
    output_prefix = os.path.join(output_prefix, '')
    if not os.path.exists(output_prefix):
        os.mkdir(output_prefix)
    return output_prefix


def split_zip_with_structure(input_zip, output_prefix, chunk_size):
    output_prefix = add_dir_split(input_zip, output_prefix, )

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


def merge_zips_with_structure(output_zip, input_prefix, total_chunks):
    with zipfile.ZipFile(output_zip, 'w') as zip_file:
        for i in range(1, total_chunks + 1):
            with zipfile.ZipFile(f'{input_prefix}{i}.zip', 'r') as chunk_zip:
                for file_info in chunk_zip.infolist():
                    with chunk_zip.open(file_info) as file:
                        zip_file.writestr(file_info.filename, file.read())


# split_zip_with_structure(save_path + save_name, split_file_path, 10)
# merge_zips_with_structure('F:\\cxxzoom\\ftp\\sync\\merge_with_structure.zip', split_file_path, 673)

# 这里就单单统计一下顶层目录下的文件个数
def scan2(path, my_dir, top_name, i):
    files = os.listdir(path)
    for file in files:
        my_dir[file] = 0
        for root, dirs, files in os.walk(os.path.join(path, file)):
            my_dir[file] += len(files)


def upload2(file_path, remote):
    files = {'file': open(file_path, 'rb')}
    url = f'http://{remote}/upload'
    print('in upload ...')
    response = requests.post(url=url, data={'file_name': file_name}, files=files)
    print(response.json(), flush=True)


# 这里写个线程池来管理上传
def a(chunk_path):
    remote = utils.config()['remote']
    # 遍历这下面的文件总数
    chunks = os.listdir(chunk_path)
    tmp_list = []
    for value in chunks:
        tmp_list.append(os.path.join(chunk_path, value))

    for file in tmp_list:
        threading.Thread(target=upload2, args=(file, remote)).start()

# a(os.path.join(utils.config()['zip_split_dir'], '20231012', ''))
