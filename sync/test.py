import os
import sys
from flask import jsonify


def scan(path, my_dir,basepath,i):
    files = os.listdir(path)

    for file in files:
        tmp = os.path.join(path, file)
        if os.path.isfile(tmp):
            name = tmp[len(basepath):]
            i = i+1
            my_dir[i] = name
            print(my_dir)
        if os.path.isdir(tmp):
            scan(tmp, my_dir,basepath,i)

my_dir = {}
scan("F:\\cxxzoom\\ftp\\test_pdf\\", my_dir,'F:\\cxxzoom\\ftp\\test_pdf\\',0)
print(len(my_dir))
