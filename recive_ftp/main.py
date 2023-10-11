import json

import requests
import yaml


def pull_sources():
    data = {
        'param1': 'value1',
        'param2': 'value2'
    }

    config = configs()

    # 发送带参数的POST请求
    response = requests.post('https://www.example.com', data=data)

    # 检查响应状态码
    if response.status_code == 200:
        # 打印响应内容
        print(response.text)
    else:
        print('请求失败，状态码:', response.status_code)


def configs(path='config.yml'):
    yaml_file_path = path

    # 打开YAML文件并解析内容
    with open(yaml_file_path, 'r') as yaml_file:
        return yaml.load(yaml_file, Loader=yaml.FullLoader)


# 要判断是不是最后一个文件夹，如果是最后一个大的文件夹，则一直不能停，


# 一个接口去查询对面有多少个文件夹，如果和当前文件夹的数目不一致，则开始拉数据
def get_files():
    config = configs('route.yaml')
    response = requests.get(config['remote']['dir'], data={'dirs': 1})
    # 检查响应状态码
    if response.status_code == 200:
        json_data = response.json()

        # 使用json.loads()解析JSON字符串为Python对象

        with open(config['remote']['files']) as file:
            file.write(json_data)
    else:
        print('请求失败，状态码:', response.status_code)


get_files()
