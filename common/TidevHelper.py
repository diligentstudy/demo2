import time

from entitys import define
from common import CmdUtil

# 保存截图
def getScreenshot(udid,imgname=""):
    if imgname=="":
        imgname = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    if define.STARTPATH != "":
        cmd = "tidevice --udid {} screenshot {}/{}.jpg".format(udid, define.STARTPATH, imgname)
    else:
        cmd = "tidevice --udid {} screenshot ./img_srccut/{}.jpg".format(udid,  imgname)
    res=CmdUtil.exec(cmd)
    print(res)