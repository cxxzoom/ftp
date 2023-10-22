# ftp
ftp project

## 编译安装python
wget https://www.python.org/ftp/python/3.8.18/Python-3.8.18.tgz

tar -xzvf Python-3.8.18.tgz
cd Python-3.8.18.tgz
./configure
make && make install




### 从源下载不到扩展
```
1. 包名错误
2. 不同平台得包名可能不一致
3. 使用得源不包含这个包,用阿里云
```
### 博客
https://blog.minkse.cn/centos-7-9-%e5%8d%87%e7%ba%a7make4-4%e7%89%88%e6%9c%ac/   升级make // 升级 gcc， gcc11就够了

安装centos : https://blog.csdn.net/qq_50377269/article/details/130971305

步骤：
```
安装好centos
下载好python3.8.18的源代码
编译安装
检查gcc和make
创建 venv
安装扩展
修改yaml
测试
```
### 卸载了新版本，下载了一个老版本，但是pip install/download错误
因为pip的版本不对。临时解决方案：
在虚拟环境里 重新安装pip(只适合与外网环境)
python \path\to\get-pip.py
