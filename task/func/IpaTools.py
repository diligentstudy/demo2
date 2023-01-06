import os

from common import CmdUtil

# ipa软件安装和系统重启助手

# 重启系统
def restartSystem(UDID,showLog):
    # tidevice restart
    try:
        cmd = "tidevice --udid {} restart".format(UDID)
        res = CmdUtil.exec(cmd)
        showLog("重启系统: {}".format(res))
        # Complete
        if res.find("Complete")>0:
            showLog("重启系统 成功")
            return True
    except Exception as e:
        showLog("重启系统 异常 {}".format(e))
    #
    return False

# 安装
def installAPP(UDID,ipaPath,showLog):
    # tidevice install example.ipa
    try:
        if os.path.exists(ipaPath):
            cmd = "tidevice --udid {} install {}".format(UDID, ipaPath)
            showLog(cmd)
            res = CmdUtil.exec(cmd)
            showLog("安装APP结果: {}".format(res))
            # Complete
            if res.find("Complete")>0:
                showLog("安装APP 成功")
                return True
        else:
            showLog("APP路径指向的文件不存在")
    except Exception as e:
        showLog("安装APP 异常 {}".format(e))
    #
    return False

# 安装目标APP
def installTargetApp(UDID,ipaPath,showLog):
    # tidevice install example.ipa
    try:
        if os.path.exists(ipaPath):
            cmd = "tidevice --udid {} install {}".format(UDID, ipaPath)
            showLog(cmd)
            res = CmdUtil.exec(cmd)
            showLog("安装目标APP结果: {}".format(res))
            # Complete
            if res.find("Complete")>0:
                showLog("安装目标APP 成功")
                return True
        else:
            showLog("APP路径指向的文件不存在")
    except Exception as e:
        showLog("安装目标APP 异常 {}".format(e))
    #
    return False

# 卸载目标APP
def uninstallTargetApp(UDID,bundleID,showLog):
    # tidevice uninstall 包名
    try:
        cmd = "tidevice --udid {} uninstall {}".format(UDID, bundleID)
        showLog(cmd)
        res = CmdUtil.exec(cmd)
        showLog("卸载目标APP结果: {}".format(res))
        if res.find("Complete") != -1:
            showLog("卸载目标APP 成功")
        # Complete
    except Exception as e:
        showLog("卸载目标APP 异常 {}".format(e))