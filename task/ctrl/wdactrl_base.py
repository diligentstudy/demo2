import os
import time

import goto
import wda
from goto import with_goto
# pip3 install dominate@2.7.0
from dominate.tags import label

from entitys import define
from common import CmdUtil


@with_goto
def initFbWDA(self):
    self.showLog("......initWDA......")
    # 查看运行中的应用
    res = CmdUtil.tidExec("tidevice --udid {} ps |grep {}".format(self.IPhoneInfo.UDID, define.WEBAGENT))
    # 启动 wda begin
    if res.find(define.WEBAGENT) > -1:
        if True:
            self.showLog("wda 已经启动 kill 掉")
            tres = CmdUtil.tidExec("tidevice --udid {} kill {}".format(self.IPhoneInfo.UDID, define.WEBAGENT))
            self.showLog(tres)  # Kill pid: 4594\n
            if tres.find("Kill pid:") > -1:
                kpid = int(tres.split(":")[1])
                for it in range(10):
                    if self.isNeedStop:
                        return
                    try:
                        os.kill(kpid, 0)
                    except Exception as e:
                        msg = "{}".format(e)
                        if msg.find("No such process") > -1:
                            time.sleep(1)  # kill 成功
                            break
                        else:
                            self.showLog(e)
                            continue
        # self.isInitWDA = True
        # self.showLog("wda 已经启动成功")
    else:
        self.showLog("wda 还没有启动")

    if self.isInitWDA == False:
        self.showLog("启动 wda ......")
        label.LB_STARTWDA
        # 启动 wda
        # tidevice xctest -B com.gameappium.WebDriverAgentRunner.xctrunner
        # tidevice wdaproxy -B com.gameappium.WebDriverAgentRunner.xctrunner --port 8200
        # 与xctest 启动方式不同的是，使用 wdaproxy 启动之后，我们可以在浏览器中使用 http://localhost:8200/status 来访问到这个 iOS：

        scmd = "tidevice --udid {} launch {} -e USE_PORT:{}".format(self.IPhoneInfo.UDID, define.WEBAGENT, self.port)
        self.showLog(scmd)
        tres = CmdUtil.exec(scmd)
        self.showLog(tres)
        # App launch env: {'USE_PORT': '8100'}
        if tres.find("App launch env:") > -1:
            self.isInitWDA = True
            self.showLog("wda 启动成功")
        else:
            isstart = False
            for it in range(10):
                if self.isNeedStop:
                    return
                res = CmdUtil.tidExec("tidevice --udid {} ps |grep {}".format(self.IPhoneInfo.UDID, define.WEBAGENT))
                # 启动 wda begin
                if res.find(define.WEBAGENT) > -1:
                    self.isInitWDA = True
                else:
                    self.showLog("等待 wda 启动...")
                    time.sleep(1)
                # p = subprocess.run('tasklist | findstr ' + define.WEBAGENT, shell=True)
                # pp = str(p)
                # if int(pp[-2]) == 0:
                #     self.showLog("等待 wda 启动...")
                #     time.sleep(1)
                # else:
                #     self.isInitWDA = True
                #     self.showLog("wda 启动成功")
                #     break
            # if isstart == False:
            #     self.showLog("重新启动 wda ......")
            #     goto .LB_STARTWDA

            # end for
            if self.isInitWDA is False:
                self.isInitWDA = True
                self.showLog("没有检测到wda,默认wda启动成功")
    # 启动 wda end


@with_goto
def initClient(self):
    label.LB_REINITCLIENT
    try:
        self.showLog("......initClient......")
        #
        #
        # 解锁后才能链接成功
        self.client = wda.USBClient(self.IPhoneInfo.UDID, port=self.port)  # 指定设备 udid 和WDA 端口号 不需要端口转发
        # client = wda.USBClient(self.IPhoneInfo.UDID, port=self.port, wda_bundle_id="com.facebook.WebDriverAgentRunner.xctrunner")
        # client = wda.Client("http://localhost:8200")      # 需要端口转发
        # 弹窗出现时会自动调用 _handle_alert函数，处理完弹窗后，代码会继续向下执行
        # wda.alert_callback = self._handle_alert
        #
        try:
            self.client.wait_ready(timeout=10)
            devinfo = self.client.device_info()
            if devinfo is not None and devinfo['uuid'] != "":
                self.showLog("initClient OK uuid=" + devinfo['uuid'])
                self.isInitClient = True
        except Exception as e:
            errmsg = "USBClient异常:{}".format(e)
            self.showLog(errmsg)
            try:
                if self.client is not None:
                    self.client.close()
            except Exception as e:
                pass
            if self.isNeedStop:
                return
            goto.LB_REINITCLIENT

        # self.client.implicitly_wait(10.0)
        # 返回主界面
        # self.client.亮屏
        # 解锁屏幕并启动facebook-wda服务
        # self.client.healthcheck()
        # self.client.unlock() # 解锁
        # self.client.home()
        #
    except Exception as e:
        errmsg = "初始化Client异常:{}".format(e)
        self.showStatus("初始化Client异常")
        self.showLog(errmsg)
        try:
            if self.client is not None:
                self.client.close()
        except Exception as e:
            pass
        # ('Connection aborted.', MuxConnectError('device port:8100 is not ready'))
        if errmsg.find("MuxConnectError('device port:{} is not ready')".format(define.WDAPORT)) > -1:
            if self.isNeedStop:
                return
            goto.LB_REINITCLIENT
