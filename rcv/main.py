import os.path
import shutil
import threading
import utils
import time


# 要判断是不是最后一个文件夹，如果是最后一个大的文件夹，则一直不能停，
# 判断文件是否存在
# 如果不存在就给新建一个文件加
# 并且给chunk下页新建一个文件加
# 再给.lock下写入当前正在需要传输得文件
def main():
    utils.before(threading.get_ident())

    while True:
        conf = utils.conf()

        maps = utils.get_maps()
        for remote_file_name in maps.keys():
            # 判断文件是否存在
            # 如果不存在就进入拉去逻辑
            if os.path.exists(os.path.join(conf['chunk_unzip_dir'], remote_file_name)):
                continue

            # 分片文件上传地址
            if not os.path.exists(os.path.join(conf['chunk_save_dir'], remote_file_name, '')):
                os.makedirs(os.path.join(conf['chunk_save_dir'], remote_file_name, ''))

            # 开始拉去逻辑
            # 创建正在传输的文件
            try:
                print(f'begin pull file{remote_file_name}')

                utils.create_lock(remote_file_name)

                # 让远程准备好文件
                ready = utils.ready(remote_file_name)
                print(f"remote chunk is ready? {ready}")
                if not ready:
                    continue

                # 开始拉取分片逻辑
                i = 0
                res = utils.remote_chunk_count(remote_file_name)
                while i < res['count']:
                    params = {
                        'file_name': remote_file_name,
                        'last': i + 1
                    }
                    if utils.pull_file(params):
                        i = i + 1

                # 判断是否传输完整
                if len(os.listdir(os.path.join(conf['chunk_save_dir'], remote_file_name))) == res['count']:
                    # 开始解压
                    utils.merge_zips_with_structure(remote_file_name)

                is_finish = utils.chunks_finish(remote_file_name)
                # if not is_finish:
                #     # 删除.lock 文件，
                #     utils.clean_files(remote_file_name)

                print(f'upload is finish')
                if is_finish:
                    # 删除chunk文件
                    # 删除压缩文件
                    clean = utils.clean_files(remote_file_name)
                    print(f'clean file is : {clean}')

            except Exception as e:
                print(e)
                utils.clean_files(remote_file_name)
