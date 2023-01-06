import os
import shutil
from pathlib import Path

def readFile(path):
    with open(path, "r+", encoding="utf-8") as shFile:
        shdata = shFile.read()
        return shdata

def writeFile(path,data):
    with open(path, "w+", encoding="utf-8") as shFile:
        shFile.write(data)

def search(path, name):
    for root, dirs, files in os.walk(path):  # path 为根目录
        if name in dirs or name in files:
            flag = 1  # 判断是否找到文件
            root = str(root)
            dirs = str(dirs)
            return os.path.join(root, dirs)
    return -1

# 删除文件夹下面的所有文件(包括空文件夹)
def cleardir(dir):
    if not os.path.exists(dir):
        return False
    if os.path.isfile(dir):
        os.remove(dir)
        return
    for i in os.listdir(dir):
        t = os.path.join(dir, i)
        if os.path.isdir(t):
            cleardir(t) # 重新调用次方法
        else:
            os.unlink(t)

    if os.path.exists(dir):
        os.removedirs(dir) # 递归删除目录下面的空文件夹

# 删除文件夹下面的所有文件(包括空文件夹)，但不删除传入的目录本身
def del_allfiledir(path):
    for elm in Path(path).glob('*'):
        #print(elm)
        elm.unlink() if elm.is_file() else shutil.rmtree(elm)

