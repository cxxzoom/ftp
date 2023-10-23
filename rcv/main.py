import os.path
import threading
import utils
import time


# 要判断是不是最后一个文件夹，如果是最后一个大的文件夹，则一直不能停，
# 判断文件是否存在
# 如果不存在就给新建一个文件加
# 并且给chunk下页新建一个文件加
# 再给.lock下写入当前正在需要传输得文件
def main():
    # 服务启动之前，获取远程文件加以及文件列表
    utils.before(threading.get_ident())

    while True:

        if not utils.can_use():
            time.sleep(60 * 60)

        conf = utils.conf()

        maps = utils.get_mapping()
        if not maps:
            print(f'{utils.now2()} : 我估计远程挂掉了，sleep 一会儿再说')
            time.sleep(conf['err_sleep'])
            print('sleep 结束')
            continue

        for remote_file_name in maps.keys():

            time.sleep(conf['sleep'])
            # 判断文件是否存在
            # 如果不存在就进入拉去逻辑
            if os.path.exists(os.path.join(conf['chunk_unzip_dir'], remote_file_name)):
                finish = utils.chunks_finish(remote_file_name)
                if not finish:
                    # 删除.lock 文件，
                    utils.clean_files(remote_file_name)
                    # unzip_path = os.path.join(conf['chunk_unzip_dir'], '', remote_file_name)
                    # if os.path.exists(unzip_path):
                    #     shutil.rmtree(unzip_path)
                else:
                    continue

            # 分片文件上传地址
            if not os.path.exists(os.path.join(conf['chunk_save_dir'], remote_file_name, '')):
                os.makedirs(os.path.join(conf['chunk_save_dir'], remote_file_name, ''))

            # 开始拉去逻辑
            # 创建正在传输的文件
            try:
                print(f'{utils.now2()} : 准备拉取文件 : {remote_file_name}')

                utils.create_lock(remote_file_name)

                # 让远程准备好文件
                ready = utils.ready(remote_file_name)
                print(f"{utils.now2()} : 远程文件准备完成? {ready}")
                if not ready:
                    print(f'{utils.now2()} : 远程文件准备失败并跳过')
                    continue

                # 开始拉取分片逻辑
                i = 0
                res = utils.remote_chunk_count(remote_file_name)
                print(f'{utils.now2()} : 文件： {remote_file_name} ，共有{res["count"]}个切片文件...')

                params = {
                    'file_name': remote_file_name,
                    'last': i + 1
                }
                utils.pull_file(params)

                while True:
                    print(f'{utils.now2()} : 正在等待文件:{remote_file_name} 分片传输完成...')
                    # 判断是否传输完整
                    if len(os.listdir(os.path.join(conf['chunk_save_dir'], remote_file_name))) == res['count']:
                        print(f'{utils.now2()} : 文件:{remote_file_name} 分片传输完成并开始解压...')
                        utils.merge_zips_with_structure(remote_file_name)
                        break

                is_finish = utils.chunks_finish(remote_file_name)
                # if not is_finish:
                #     # 删除.lock 文件，
                #     utils.clean_files(remote_file_name)
                #     unzip_path = os.path.join(conf['chunk_unzip_dir'], '', remote_file_name)
                #     if os.path.exists(unzip_path):
                #         shutil.rmtree(unzip_path)

                if is_finish:
                    # 删除chunk文件
                    # 删除压缩文件
                    clean = utils.clean_files(remote_file_name)
                    utils.upload_done(remote_file_name)
                    print(f'{utils.now2()} : 文件:{remote_file_name} 解压传输完成，完成时间{utils.now2()}...')


            except Exception as e:
                print(e)
                utils.clean_files(remote_file_name)
