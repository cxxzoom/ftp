import json
import os.path

import requests
import yaml
import utils

remote = '192.168.1.15:9999'


# 要判断是不是最后一个文件夹，如果是最后一个大的文件夹，则一直不能停，
def main():
    # 从远程拉取文件树  文件夹 ： 当前文件夹所有文件个数
    if not os.path.exists('maps.json'):
        get_mapping()

    maps = get_maps()
    for map in maps:
        a = {}
        # TODO 这里开始就要开始拉取数据和逻辑了
        # 遍历这个maps
        # 调用远程的ready 接口
        # 开始文件传输和保存文件内容
        #


# 一个接口去查询对面有多少个文件夹，如果和当前文件夹的数目不一致，则开始拉数据
def get_mapping():
    response = requests.get(f'http://{remote}/maps')
    code, msg, res = response.json()['code'], response.json()['msg'], response.json()['res']
    if code == 0:
        print(res)
        with open('maps.json', 'w') as file:
            json.dump(res, file)


def get_maps():
    with open('maps.json', 'r') as file:
        maps = json.load(file)
        return maps if maps else {}


# 获取当前是否有文件处于传输状态
get_mapping()
