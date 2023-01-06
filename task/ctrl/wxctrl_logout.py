import time
from entitys import define
from entitys.eLanguage import enumLanguage as LANG
import goto
from goto import with_goto
from dominate.tags import label
# 退出登录账号
from task.ctrl import wxctrl_base as wxctrlBase


# 退出当前登录的APP 账号
from task.ctrl import sysctrl_flightmode as sysCtrlFlight
from task.func import IpaTools
from common import  CmdUtil

# 退出WX
@with_goto
def logoutAppFunc(client,showLog,udid,fnInitData):
    if client is not None:
        # 检测是否已经登录
        try:
            wxctrlBase.setCurrentApp(client,udid, showLog)
            # 检测是否已经登录 # "通过设备菜单开启微信通知：“设置”>“通知”>“微信”"
            if client(className="XCUIElementTypeStaticText", name=LANG.不再显示.T()).exists:
                client(className="XCUIElementTypeStaticText", name=LANG.不再显示.T()).click()

            client(className="XCUIElementTypeButton", name=LANG.我.T()).wait(3)
            if client(className="XCUIElementTypeButton", name=LANG.我.T()).exists:

                # 关闭App,清理数据
                showLog("退出App账号,清理数据")
                # 跳到wx主界面，点击我，点设置，点退出
                # d.app_terminate("com.apple.Health")  #
                # 启动APP到前台 d.app_activate  这里异常不能用
                # CmdUtil.exec("tidevice --udid {} launch {}".format(IPhoneInfo.UDID, bundleID))
                # client.app_launch(IPhoneInfo.UDID)
                logoutAccount(client, showLog)
                time.sleep(0.5)
                #
                #重新初始化数据
                fnInitData()
                #
                showLog("退出目标APP")
                tres = CmdUtil.exec("tidevice --udid {} kill {}".format(udid, define.PACKAGENAME))
                showLog(tres)
                #
                # 重装APP或者重新刷底包
                label.LB_INSTALLAPP2
                if define.LOGOUTACCESS == "reinstall":
                    showLog("卸载目标APP...")
                    IpaTools.uninstallTargetApp(udid, define.PACKAGENAME, showLog)
                    showLog("安装目标APP...")
                    installResult = IpaTools.installTargetApp(udid, define.THEIPAFILE, showLog)
                    if installResult is True:
                        showLog("安装目标APP成功")
                    else:
                        showLog("安装目标APP失败")
                        goto.LB_INSTALLAPP2

                # end if
                return True
        except Exception as e:
            showLog("退出账号异常:{}".format(e))
    #end if
    return False

# 退出WX
def logoutAccount(client,showLog):
    try:
        if client(name=LANG.设置.T()).exists:
            showLog("点击 设置")
            wxctrlBase.clickCoordinate(client, LANG.设置)
        else:
            showLog("点击 我")
            wxctrlBase.clickBarMe(client)
            showLog("点击 设置")
            client(className="XCUIElementTypeStaticText", name=LANG.设置.T()).wait()
            client(className="XCUIElementTypeStaticText", name=LANG.设置.T()).click()


        client.swipe_up()
        time.sleep(0.5)
        wxctrlBase.clickCoordinate(client, LANG.退出WX)
        wxctrlBase.clickCoordinate(client, LANG.退出WX红色)

    except Exception as e:
        showLog("退出账号 异常 {}".format(e))