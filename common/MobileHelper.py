import json
import re
from urllib import parse

from entitys import define
from entitys.resetType import TaskMode
from common import HttpHelper

def makeUrl(url):
    return "http://{}{}".format(define.MOBILEMSG_IP, url)

# 自动登录：提取一个手机号码和密码
def getUserAndPwd():
    # 提取手机号码
    url = makeUrl('/api/mob/getuserandpwd?sjk={}'.format(define.SJK_LOGIN))
    status, text = HttpHelper.httGet(url)
    if status == 200:
        if text is not None and text != "":
            # 加上区号
            if text[0:len(define.AREACODE)] != define.AREACODE:
                text = define.AREACODE + text
            return text  # user----pwd
        else:
            return None
    else:
        return None


# 上传账号 和 失败原因 如： 获取不到验证码，封号
# 格式： 账号----密码----失败原因
def reportUser(mobile, pwd, state, reason):

    if reason is not None and reason != "" and reason.find("\n") >= 0:
        reason = reason.replace("\n", "")
    url = makeUrl('/api/mob/reportuser?sjk={}&hm={}----{}----{}----{}'.format(define.SJK_LOGIN_REPORT,parse.quote(mobile), pwd,state,reason))
    status, text = HttpHelper.httGet(url)
    if status == 200:
        return text
    else:
        return None

