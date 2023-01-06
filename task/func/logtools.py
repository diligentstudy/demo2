# 保存公共获取账号日志记录
import threading
from datetime import datetime

lock_usergetlog = threading.Lock()

def writeUserGetLog(usergetlogfile, msg):
    try:
        with lock_usergetlog:
            with open(usergetlogfile, "a", encoding='utf-8') as file:  # ”a"代表追加
                datestr = datetime.now().strftime('%Y-%m-%d %H:%M:%S  ')
                file.write(datestr)
                file.write(msg)
                file.write("\n")
                file.close()
    except Exception as e:
        pass

def writeLog(logname, msg):
    #
    if logname != "":
        try:
            with open(logname, "a", encoding='utf-8') as file:  # ”a"代表追加
                datestr = datetime.now().strftime('%Y-%m-%d %H:%M:%S   ')
                file.write(datestr)
                file.write(msg)
                file.write("\n")
                file.close()
        except Exception as e:
            pass