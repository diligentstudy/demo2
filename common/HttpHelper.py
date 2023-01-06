import os

import requests

from entitys import define

httpheader=""
authHeader=""
authJsonHeader=""

def initHeader():
    global httpheader,authHeader,authJsonHeader
    httpheader = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36'
        }

    authHeader = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36'
        , 'Authorization': 'Basic {}'.format(define.AUTHORIZATION)}
    #

    authJsonHeader = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36'
        , 'Authorization': 'Basic {}'.format(define.AUTHORIZATION)
        , 'content-type': 'application/json'}

    #

def httGet(url):
    try:
        ses = requests.session()
        ses.keep_alive = False  # 关闭多余连接
        # proxies=my_proxies,
        res = ses.get(url, headers=httpheader)  # 你需要的网址
        res.encoding = 'utf8'
        resstatus = res.status_code
        restext = res.text
        res.close()
        ses.close()
        # print('status_code={}'.format(resstatus))
        return resstatus, restext
    except Exception as result:
        #print('Poset 异常{}'.format(result))
        return None, None

def httPost(url, data):
    try:
        ses = requests.session()
        ses.keep_alive = False  # 关闭多余连接
        # proxies=my_proxies,
        res = ses.post(url, data=data, headers=httpheader)
        res.encoding = 'utf8'
        resstatus = res.status_code
        restext = res.text
        res.close()
        ses.close()
        return resstatus, restext
    except Exception as result:
        #print('Poset 异常{}'.format(result))
        return None, None


def httJsonGet(url):
    try:
        ses = requests.session()
        ses.keep_alive = False  # 关闭多余连接
        # proxies=my_proxies,
        res = ses.get(url, headers=authHeader)  # 你需要的网址
        res.encoding = 'utf8'
        resstatus = res.status_code
        restext = res.text
        res.close()
        ses.close()
        # print('status_code={}'.format(resstatus))
        return resstatus, restext
    except Exception as result:
        #print('Poset 异常{}'.format(result))
        return None, None


# 下载文件
# url 下载地址
# savefile 保存本地物理路径
def httAuthDown(url,savefile):
    try:
        ses = requests.session()
        ses.keep_alive = False  # 关闭多余连接
        #print("下载文件")
        #print(url)
        res = ses.get(url, headers=authHeader)  # 你需要的网址
        res.encoding = 'utf8'
        resstatus = res.status_code
        restext = ""
        isdownok = False
        #
        if resstatus == 200:
            # Content-Disposition': 'attachment; filename=xxx.zip',
            if "Content-Disposition" in res.headers and res.headers["Content-Disposition"].find("_wxid_")>0 :
                with open(savefile, "wb") as code:
                    code.write(res.content)
                #
                if os.path.exists(savefile):
                    isdownok=True

                # print(restext)
            else:
                if res.json() is not None:
                    restext = res.json["msg"]
                else:
                    restext = res.text

        res.close()
        ses.close()
        # print('status_code={}'.format(resstatus))
        return resstatus,restext, isdownok
    except Exception as result:
        print('httAuthDown 异常{}'.format(result))
        return None, None, None

def httAuthPost(url, data,header=None):
    try:
        ses = requests.session()
        ses.keep_alive = False  # 关闭多余连接
        # proxies=my_proxies,
        if header is None:
            res = ses.post(url, data=data, headers=authHeader)
        else:
            res = ses.post(url, data=data, headers=header)

        res.encoding = 'utf8'
        resstatus = res.status_code
        restext = res.text
        res.close()
        ses.close()
        return resstatus, restext
    except Exception as result:
        #print('Poset 异常{}'.format(result))
        return None, None

def httAuthJosnPost(url, data,header=None,upfile=None):
    try:
        ses = requests.session()
        ses.keep_alive = False  # 关闭多余连接
        # proxies=my_proxies,
        if header is None:
            if upfile is None:
                res = ses.post(url, json=data, headers=authJsonHeader, files=upfile)
            else:
                res = ses.post(url, json=data, headers=authJsonHeader)
        else:
            if upfile is None:
                res = ses.post(url, json=data, headers=header, files=upfile)
            else:
                res = ses.post(url, json=data, headers=header)
        #print(res.request.body, res.request.headers)
        res.encoding = 'utf8'
        resstatus = res.status_code
        restext = res.text
        # retDict = res.json()
        res.close()
        ses.close()
        return resstatus, restext
    except Exception as result:
        #print('Poset 异常{}'.format(result))
        return None, None
