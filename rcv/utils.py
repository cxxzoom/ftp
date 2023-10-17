import json
import shutil
import zipfile
import os
import requests
import yaml
from datetime import datetime


# 合并文件
def merge_zips_with_structure(remote_file_name):
    config = conf()
    output_zip = os.path.join(config['chunk_unzip_dir'], remote_file_name) + '.zip'
    input_prefix = os.path.join(config['chunk_save_dir'], remote_file_name, '')
    total_chunks = len(os.listdir(os.path.join(config['chunk_save_dir'], remote_file_name)))
    with zipfile.ZipFile(output_zip, 'w') as zip_file:
        for i in range(1, total_chunks + 1):
            with zipfile.ZipFile(f'{input_prefix}{i}.zip', 'r') as chunk_zip:
                for file_info in chunk_zip.infolist():
                    with chunk_zip.open(file_info) as file:
                        zip_file.writestr(file_info.filename, file.read())

    unzip_file(output_zip, os.path.join(config['chunk_unzip_dir'], remote_file_name, ''))


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
    config = conf()
    response = requests.get(f'http://{config["remote"]}/maps')
    code, msg, res = response.json()['code'], response.json()['msg'], response.json()['res']
    if code == 0:
        # print(res)
        with open('maps.json', 'w') as file:
            json.dump(res, file)


# 考虑这里是不是需要
# 或者直接每次传输的时候直接去拉去不就得了？
# 获取需要传输的文件列表--本地
def get_maps():
    if not os.path.exists('maps.json'):
        try:
            get_mapping()
        except Exception as e:
            print(f'get remote file with err:{e}')
            return {}
    with open('maps.json', 'r') as file:
        remote_file_names = json.load(file)
        return remote_file_names if remote_file_names else {}


# 从远程拉去chunk文件
def pull_file(params: dict) -> bool:
    print('pulling file...')
    config = conf()
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/76.0.3809.100 Safari/537.36',

        'Content-Type': 'application/json'
    }
    response = requests.post(f'http://{config["remote"]}/send',
                             json=params,
                             headers=header)
    res = response.text
    print('maybe done...')
    print(res)
    # if res['code'] != 0:
    #     return False
    return True


# 判断是否全部传输完成。如果没全部传输完成，则重新
def chunks_finish(file_name):
    config = conf()
    files = scan2(os.path.join(config['chunk_unzip_dir'], file_name, ''))

    with open('maps.json', 'r') as file:
        res = json.load(file)
    if res[file_name] == files['count']:
        return True
    return False


# TODO
def get_chunk_number(file_name: str) -> int:
    config = conf()
    files = os.listdir(os.path.join(conf['zip_split_dir'], file_name))
    with open('maps.json', 'r') as file:
        res = json.load(file)
        num = res[file_name]
    return len(files)


def ready(file_name: str) -> bool:
    config = conf()
    response = requests.get(f'http://{config["remote"]}/ready',
                            json={'file_name': file_name})
    print(f'rcv->ready->{response.text}')
    if response.status_code == 200:
        return True
    return False


# 获取远程当前文件的分片数量
def remote_chunk_count(file_name: str) -> dict:
    config = conf()
    params = {'file_name': file_name}
    response = requests.get(f'http://{config["remote"]}/chunk_count',
                            json=params)
    res = response.json()
    return res['res']


# 扫描文件个数
#
def scan2(path):
    my_dir = {}
    my_dir['count'] = 0
    if os.path.exists(path):
        files = os.listdir(path)
        for file in files:
            # 如果是文件的话，不需要扫描，但是要加1
            if os.path.isfile(os.path.join(path, file)):
                my_dir['count'] += 1
            for root, dirs, files in os.walk(os.path.join(path, file)):
                my_dir['count'] += len(files)
    return my_dir


def clean_files(file_name: str):
    config = conf()
    # 删除chunk文件
    # 删除zip文件
    try:
        # 递归删除chunk文件
        # 删除压缩包
        # 删除.lock真正在执行的任务
        chunk_dir = os.path.join(config['chunk_save_dir'], file_name, '')
        zip_file = os.path.join(config['chunk_unzip_dir'], file_name) + '.zip'

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
def before(t_id: int):
    config = conf()
    if not os.path.exists(config['chunk_save_dir']):
        os.mkdir(config['chunk_save_dir'])

    if not os.path.exists(config['chunk_unzip_dir']):
        os.mkdir(config['chunk_unzip_dir'])
    if not os.path.exists('.lock'):
        with open('.lock', 'w') as file:
            file.write('')
    # 记录线程的id
    if not os.path.exists('thread_id.txt'):
        with open('thread_id.txt', 'w') as t:
            json.dump({'tread_id': t_id, 'time': datetime.now().strftime("%Y%m")}, t)


def log(params: dict):
    config = conf()
    log_dir = os.path.join(config['log_save_dir'])

    if not os.path.exists(log_dir):
        os.mkdir(log_dir)

    month_log = os.path.join(log_dir, datetime.now().strftime("%Y%m"), '')
    if not os.path.exists(month_log):
        os.mkdir(month_log)

    # with open(os.path.join(month_log, datetime.now().strftime("%d")), 'a') as file:
    #     json.dump(params, file)


# 文件上传完成之后需要删除源文件
def upload_done(file_name):
    url = f"http://{conf()['remote']}/done"
    params = {'file_name': file_name}
    requests.get(url=url, data=params)
    return
