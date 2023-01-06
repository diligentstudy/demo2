
import json
import os
from urllib import parse

import requests

from entitys import define
from common import HttpHelper

# 添加用户日志
# 返回 {"code":0, "msg": ""} 返回code =0 表示成功，其他失败
def addUserLogs(user, pwd, wxid, udid, logtype, state, oneuser, content, bak=""):
    url = '{}/api/log/adduserlogs'.format(define.HOSTSERVER)
    data = {"user": user, "pwd": pwd, "wxid": wxid, "udid": udid,
            "logtype": logtype, "state": state, "oneuser": oneuser,
            "content": content, "bak": bak}
    status, jsontext = HttpHelper.httAuthPost(url, data)
    if status == 200:
        json_object = json.loads(jsontext)
        return json_object
    else:
        return None
