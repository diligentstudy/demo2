#!/usr/bin/python3
# -*- coding:utf8 -*-
import datetime
from datetime import datetime as theDateTime
import json
import os
import threading

import wda
import time
# pip3 install goto-statement==1.2
import goto
from goto import with_goto
# pip3 install dominate==2.7.0
from dominate.tags import label
from PyQt5.QtCore import pyqtSignal, QThread

from entitys import define
from entitys.resetType import ResetType
from entitys.stack import Stack

from task.ctrl import wdactrl_base as wdaCtrl
from common.ExLogHelper import log_exception
from task.func import logtools
lock_usergetlog = threading.Lock()


class wxAutoLoginThread(QThread): # wxAutoLoginThread
    # 创建一个信号，触发时传递给槽函数
    updateStatus = pyqtSignal(int, int, int, str)
    updateLogs = pyqtSignal(str)
    #
    # def __init__(self, IPhoneInfo, platform ='ios'):
    #     threading.Thread.__init__(self)
    #     #
    #     self.IPhoneInfo = IPhoneInfo
    # debug模式，会在run运行时控制台生成消息
    wda.DEBUG = False  # default False
    #wda.logger
    # 如果连接本地地址失败，通常会运行1分钟才弹超时信息，在这可以设置超时10s就提示信息
    wda.HTTP_TIMEOUT = 120.0  # default 180 seconds
    wda.DEVICE_WAIT_TIMEOUT = 30.0

    def __init__(self, IPhoneInfo, bundleId, port, taskMode):
        super().__init__()

        self.IPhoneInfo = IPhoneInfo
        self.mobileModel = IPhoneInfo.MarketName
        self.bundleID = bundleId  # "com.tencet.xin001"
        self.port = port  # 8200
        self.taskMode = taskMode

        # 获取进程编号
        self.PID = os.getpid()
        # print('进程编号:', os.getpid())
        # # 获取sing父进程的编号
        # print("父进程:", os.getppid())
        # # 获取当前进程  查看是由那个进程执行的
        # print('查看是由那个进程执行的:', multiprocessing.current_process())

        # 是否完成初始化
        self.isInitWDA = False
        self.isInitClient = False
        self.installResult = False
        # 重置脚本回滚类型
        self.recoveryType = ResetType.Normal
        #
        self.client = None
        self.user_pwd = []
        self.steps = Stack()  # 步骤堆栈
        #
        # 上一个登录成功的号，判断是否需要重新安装APP的标准
        self.lastLoginUser = ""
        #

        # ......initData......
        self.isLogined = False  # 是否已经登录成功
        self.isNeedStop = False  # 是否需要退出线程
        self.isBlock = False
        #

        self.wxid = ""
        self.friendcount = 0
        self.bindmobile = ""
        self.bakImgName = ""
        self.str62 = ""
        self.curtime = time.strftime('%Y%m%d', time.localtime(time.time()))
        self.logname = ""
        self.usergetlogfile = "{}/logs/getuser_{}.log".format(define.STARTPATH, self.curtime)

    def initData(self):
        self.showLog("......initData......")
        self.isLogined = False  # 是否已经登录成功
        self.isNeedStop = False  # 是否需要退出线程
        self.isBlock = False
        #
        self.user_pwd = []
        # 步骤堆栈
        self.steps = Stack()
        #
        self.wxid = ""
        self.friendcount = 0
        self.bindmobile = ""
        self.bakImgName = ""
        self.str62 = ""
        self.curtime = time.strftime('%Y%m%d', time.localtime(time.time()))
        self.logname = ""
        self.usergetlogfile = "{}/logs/getuser_{}.log".format(define.STARTPATH, self.curtime)

        #
        self.showLog("initData 成功")

    @log_exception
    def run(self):
        self.showLog("......runing......")
        stacks = None
        try:
            if self.isInitWDA is False:
                wdaCtrl.initFbWDA(self)
            if self.isInitWDA is False:
                self.showLog("{}号手机连接WDA失败，请检查是否需要锁屏密码，或请拔线重试".format(self.IPhoneInfo.RowNo))
                return

            if self.isInitClient is False:
                wdaCtrl.initClient(self)
            if self.isInitClient is False:
                self.showLog("{}号手机连接失败，请检查是否需要锁屏密码，或请拔线重试".format(self.IPhoneInfo.RowNo))
                return
            else:
                #
                curStatus = self.client.status()
                self.showLog("连接IP={},连接消息={}".format(curStatus["ios"]["ip"], curStatus["message"]))

                self.task_login()

                self.showStatus("脚本已经结束")
                if stacks is not None:
                    self.showLog("已完成步骤：{}".format(' '.join(stacks.getList())))
                #
        except Exception as e:
            errmsg = "错误:脚本停止：{}".format(e)
            self.showStatus("错误:脚本停止")
            self.showLog(errmsg)
            # ('Connection aborted.', MuxConnectError('device port:8100 is not ready'))
            # if errmsg.find("MuxConnectError('device port:{} is not ready')".format(define.WDAPORT)) > -1:
            #     goto.LB_REINITWDA
            if stacks is not None:
                self.showLog("已完成步骤：{}".format(' '.join(stacks.getList())))
            #print(e)
            raise

    @with_goto
    def task_login(self):
        # 业务代码
        pass

    def pushStep(self, stepname):
        # 步骤列表
        self.steps.push(stepname)

    # 获取是否已经登录
    def getLogined(self):
        return self.isLogined

    def showUser(self, name):
        self.updateStatus.emit(self.IPhoneInfo.RowNo, self.IPhoneInfo.RowIndex, 8, name)

    def showStatus(self, msg):
        self.updateStatus.emit(self.IPhoneInfo.RowNo, self.IPhoneInfo.RowIndex, 9, msg)

    def showStatuLog(self, msg):
        self.updateStatus.emit(self.IPhoneInfo.RowNo, self.IPhoneInfo.RowIndex, 9, msg)
        self.updateLogs.emit("{} 号手机 {}".format(self.IPhoneInfo.RowNo, msg))
        #
        if self.logname != "":
            logtools.writeLog(self.logname, "{} 号手机 {}".format(self.IPhoneInfo.RowNo, msg))

    def showLog(self, msg):
        self.updateLogs.emit("{} 号手机 {}".format(self.IPhoneInfo.RowNo, msg))
        #
        if self.logname != "":
            logtools.writeLog(self.logname,"{} 号手机 {}".format(self.IPhoneInfo.RowNo, msg))
