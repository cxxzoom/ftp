import os


def scan(path, mydir):
    files = os.listdir(path)

    for file in files:
        tmp = os.path.join(path, file)
        if os.path.isfile(tmp):
            print(tmp)

        if os.path.isdir(tmp):
            print("this is dir->%s", tmp)
            scan(tmp, mydir)


mydir = {}
scan("F:\\script_boy", mydir)

dire = {}

print(dire)
