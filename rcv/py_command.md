离线命令下载：
```shell
pip download -d package PyYAML --only-binary=:all: --platform linux_x86_64 --python-version 3.7 -i https://pypi.tuna.tsinghua.edu.cn/simple
```
百度镜像：
```shell
pip download pyyaml -d package -i https://mirror.baidu.com/pypi/simple
```

```shell
flask
request
pyyaml
```
````shell
pip download pyyaml -d package --only-binary=:all: --platform linux_x86_64  -i https://mirrors.aliyun.com/pypi/simple/
````




离线安装： pip install --no-index --find-links=/packages/ -r requirements.txt