import json
import os.path

import requests
import yaml
import utils

remote = '192.168.1.15:9999'


# 要判断是不是最后一个文件夹，如果是最后一个大的文件夹，则一直不能停，
# 判断文件是否存在
# 如果不存在就给新建一个文件加
# 并且给chunk下页新建一个文件加
# 再给.lock下写入当前正在需要传输得文件
def main():
    test_pull('20231012')
    exit()
    conf = utils.conf()
    if not utils.has_lock() or not utils.get_lock_file():
        # 从远程拉取文件树  {文件夹:当前文件夹所有文件个数}
        if not os.path.exists('maps.json'):
            try:
                utils.get_mapping()
            except Exception as e:
                print(e)

        maps = utils.get_maps()

        for map in maps.keys():
            a = {}
            # TODO 这里开始就要开始拉取数据和逻辑了
            # 遍历这个maps
            # 调用远程的ready 接口
            # 开始文件传输和保存文件内容
            #
            print(map)
            # 判断文件是否存在
            # 如果不存在就进入拉去逻辑
            if not os.path.exists(conf['chunk_save_dir']):
                # 开始拉去逻辑
                # 创建正在传输的文件
                utils.create_lock(map)
                save_path = os.path.join(conf['chunk_save_dir'], map)
                if not os.path.exists(save_path):
                    os.mkdir(save_path)
                # 循环拉去文件。如果成功则拉去下一个
                i = 0
                while i != maps[map]:
                    params = {
                        'file_name': map,
                        'last': i + 1
                    }
                    if utils.pull_file(params):
                        i = i + 1
                # 判断是否传输完整


# 一个接口去查询对面有多少个文件夹，如果和当前文件夹的数目不一致，则开始拉数据
def test_pull(map):
    i = 0
    params = {
        'file_name': map,
        'last': i + 1
    }
    print(utils.pull_file(params))


# 获取当前是否有文件处于传输状态
main()
