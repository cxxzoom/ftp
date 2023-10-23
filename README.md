# sync

sync project

## 编译前置需求

1. gcc >= 11.0
2. make >= 4.3
   直接把gcc更新到>11.0就行了

## 编译安装python

wget https://www.python.org/ftp/python/3.8.18/Python-3.8.18.tgz

tar -xzvf Python-3.8.18.tgz
cd Python-3.8.18.tgz
./configure
make && sudo make install

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
跑起来
```

## 流程

```txt
先配置yaml
1. 启动发送方
2. 启动接收方

循环：
1. 接收方获取发送方的所有文件目录以及文件个数
2. 接收方对比资源存放目录和接收方目录
3. 扫描同名文件下的文件个数并对比
4. 同名文件下数量不同，则删除接收方的同名文件
5. 拉取文件
6. 发送方压缩并切片文件
7. 多线程发送文件
8. 获取远程文件的分片全部传输完就开始解压
9. sleep
```


### 瓶颈
压缩解压分片是当前项目的瓶颈，而且接收方解压是磁盘占用比较高

## 接收方配置文件 rcv
```yaml
chunk_save_dir: F:\cxxzoom\ftp\public2\chunk\   分片文件保存的位置
chunk_unzip_dir: F:\cxxzoom\ftp\public2\        分片合并和解压到的位置
remote: 192.168.1.71:9999                       发送方服务
log_save_dir: F:\cxxzoom\ftp\log\               日志位置，暂时没咋用
sleep: 20                                       休眠时间
```

## 发送方配置文件 send
```yaml
source_dir: /mnt/f/cxxzoom/ftp/test_pdf         要发送的资源文件
zip_compress_dir: /mnt/f/cxxzoom/ftp/public/zip 压缩文件存放位置
zip_split_dir: /mnt/f/cxxzoom/ftp/public/chunk  分片文件存放位置
remote: 192.168.1.71:7777                       接收方服务
chunk_size: 100                                 一个分片里放多少个文件
```

## 运行时：
记录send的线程id
....


## 错误
1. 如果如果接收方被抛异常了，会导致项目不可用？
2. 安装package时，接收方的包可能会提示安装失败或者版本不可用？ 都安装send下的package就行了