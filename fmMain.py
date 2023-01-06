import functools
import json
import os
import datetime
import cv2
import sys  # sys模块提供了一系列有关Python运行环境的变量和函数。
import threading
import time
import subprocess

import wda
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QCursor, QIcon

# import utils.CmdUtil
from entitys import define
from entitys.iphoneInfo import IPhoneInfo
from entitys.resetType import ResetType, TaskMode
from fmAutoTask import FmAutoTask

from task.ctrl.sysctrl_flightmode import openFlightMode, closeFlightMode

from task.func.IpaTools import uninstallTargetApp, installTargetApp, installAPP
from task.taskth_wx_reg import wxAutoRegThread
from ui.mainUI import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow, QStatusBar, QLabel, QHeaderView, QMenu, QAction, \
    QTableWidgetItem, QMessageBox, QInputDialog
import configparser
from common import CmdUtil, HttpHelper
from task.taskth_wx_login import wxAutoLoginThread  # 模式
from entitys.enumTask import enumTask as ETASK
#
from common.ExLogHelper import log_exception


class xmainForm(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(xmainForm, self).__init__(parent)
        self.setupUi(self)
        # self.setWindowOpacity(0.93)
        self.resize(1000, 600)
        self.setWindowTitle("IOS群控")
        # 设置图标
        # self.setWindowIcon(QIcon('images\logo1.png'))
        # self.setWindowIcon()

        # 支持的任务类型 如wx,抖音
        self.taskTypes = ["wx自动登录", "wx自动注册"]

        # 当前连接的ipone手机字典
        self.iphoneDict = {}
        # 当前已经启动过的任务线程字典
        self.taskDict = {}
        # 累加的行号
        self.rowNo = 1
        #
        configINI = configparser.ConfigParser()  # configINI.readfp(open('config.ini',mode="r",encoding="utf-8"))
        configINI.read_file(open(define.STARTPATH + '/config.ini', mode="r", encoding="utf-8"))
        #
        # self.lbMsg.setText("{},python版本 {},cv2路径：\n{}".format(self.configINI.get("autotask", "remark"),sys.version,cv2.__file__))
        self.showLog("python版本 {}".format(sys.version.replace("\n", "")))
        self.showLog("Python解释器路径 {}".format(define.EXECUTABLE))
        self.showLog("cv2路径：{}".format(cv2.__file__))
        #
        self.initDefine(configINI)
        #
        # 初始界面
        self.initUi()
        #
        self.fmAutoTask = FmAutoTask()

    def initDefine(self, configINI):
        # 日志目录
        if os.path.exists(define.STARTPATH + "/logs") is False:
            os.makedirs(define.STARTPATH + "/logs")
        if os.path.exists(define.STARTPATH + "/images") is False:
            os.makedirs(define.STARTPATH + "/images")

        define.MOBILEMSG_IP = configINI.get("server", "mobilemsg_ip")
        define.HOSTSERVER = configINI.get("server", "hostserver")
        define.AUTHORIZATION = configINI.get("server", "authorization")

        define.DEFMOBILEMODEL = configINI.get("setting", "defmobilemode")

        #
        define.RULLTASKMODE = configINI.get("setting", "fulltaskmode")
        define.CURTASKMODE = configINI.get("setting", "curtaskmode")
        define.LANGUAGE = configINI.get("setting", "language")
        define.PACKAGENAME = configINI.get("setting", "packagename")
        define.WDAPORT = int(configINI.get("setting", "wdaport"))
        define.APISLEEP = int(configINI.get("setting", "apisleep"))
        define.AREACODE = configINI.get("setting", "areacode")
        define.IMGSTORE = configINI.get("setting", "imgstore")

        define.WAITAFTERFRIENDREQ = int(configINI.get("setting", "waitafterfriendreq"))
        if configINI.get("setting", "mustrelogin") == "0":
            define.MUSTRELOGIN = False
        else:
            define.MUSTRELOGIN = True
        #
        if configINI.get("setting", "keepactive") == "0":
            define.KEEPACTIVE = False
        else:
            define.KEEPACTIVE = True
        #
        if configINI.get("setting", "allowrelogin") == "0":
            define.ALLOWRELOGIN = False
        else:
            define.ALLOWRELOGIN = True
        #

        if configINI.get("setting", "mustreimgbak") == "0":
            define.MUSTREIMGBAK = False
        else:
            define.MUSTREIMGBAK = True

        if configINI.get("dragimage", "allowautodrag") == "0":
            define.ALLOWAUTODRAG = False
            self.showLog("不允许自动拖图")
        else:
            self.showLog("允许自动拖图")
            define.ALLOWAUTODRAG = True

        # 自动任务设置
        # 目前支持的自动任务类型：
        define.TASK_FULL = configINI.get("autotask", "fulltask").split(",")
        # 当前配置的任务
        define.TASK_CURSET = configINI.get("autotask", "curlist").split(",")
        # 任务运行开关，0 不开启，1 开启
        if configINI.get("autotask", "runswg") == "0":
            define.TASK_RUNSWG = False
        else:
            define.TASK_RUNSWG = True

        #
        try:
            if os.path.exists(define.IMGSTORE) is False:
                self.showLog("配置的挂载目录不存在:{}".format(define.IMGSTORE))
                os.makedirs(define.IMGSTORE)
            if os.path.exists(define.IMGSTORE + "/tmp") is False:
                os.makedirs(define.IMGSTORE + "/tmp")
            if os.path.exists(define.IMGSTORE + "/base") is False:
                os.makedirs(define.IMGSTORE + "/base")
        except Exception as e:
            self.showLog("创建挂载目录异常:{}".format(e))

        # 获取短信循环等待秒数
        define.APISMSSLEEP = int(configINI.get("setting", "apismsleep"))
        # 获取短信超时秒数
        define.APISMSWAIT = int(configINI.get("setting", "apismswait"))
        define.SKIPUSERS = configINI.get("setting", "skipusers")
        define.TESTUSER = configINI.get("setting", "testuser")
        #
        define.DRAGIMGWAITLOAD = int(configINI.get("dragimage", "waitloadimg"))
        define.DRAGALIGIN = configINI.get("dragimage", "dargalign")
        # 目标APP路径
        define.THEIPAFILE = "{}/res/{}".format(define.STARTPATH, configINI.get("install", "ipafile"))
        define.BACKUPAPP = "{}/res/{}".format(define.STARTPATH, configINI.get("install", "ipabackup"))
        #
        define.LOGOUTACCESS = configINI.get("setting", "outaccess")

        if configINI.get("backups", "backfriend") == "0":
            define.BACKFRIEND = False
        else:
            define.BACKFRIEND = True

        # 是否必须重装APP
        if configINI.get("install", "reinstall") == "0":
            define.NEEDREINSTALL = False
        else:
            define.NEEDREINSTALL = True
        #
        if configINI.get("setting", "fightmode") == "0":
            define.FIGHTMODESWG = False
        else:
            define.FIGHTMODESWG = True

        define.SJK_LOGIN = configINI.get("sjk", "login")
        define.SJK_LOGIN_REPORT = configINI.get("sjk", "login_report")
        define.SJK_REG = configINI.get("sjk", "reg")
        define.SJK_REG_REPORT = configINI.get("sjk", "reg_report")
        define.SJK_REG_UP_QRCODE = configINI.get("sjk", "reg_up_qrcode")
        define.SJK_REPORT_NEEDFRIEND = configINI.get("sjk", "reportneedfriend")

        #
        HttpHelper.initHeader()

    # Database MySQL
    # define.DB_HOST = configINI.get("mysql", "DBHOST")
    # define.DB_PORT = int(configINI.get("mysql", "DBPORT"))
    # define.DB_USER = configINI.get("mysql", "DBUSER")
    # define.DB_PASSWD = configINI.get("mysql", "DBPWD")
    # define.DB_DBNAME = configINI.get("mysql", "DBNAME")
    # define.DB_CHARSET = configINI.get("mysql", "DBCHAR")

    # 初始界面
    def initUi(self):
        # self.gBoxBtns.setFixedWidth(100)
        # self.gboxvLayout.setFixedWidth(190)
        self.rightMenu = None

        # self.cbBoxTaskType.addItems(self.taskTypes)
        #

        self.statusBar = QStatusBar()
        self.labStatus = QLabel('当前状态：未连接')
        self.setStatusBar(self.statusBar)
        self.statusBar.addPermanentWidget(self.labStatus, stretch=1)
        self.labPackage = QLabel('')
        self.statusBar.addPermanentWidget(self.labPackage, stretch=2)
        # UDID                       SerialNumber    NAME        MarketName    ProductVersion    ConnType
        self.header = ["选择", "NO.", "UDID", "序列号", "名称", "型号", "产品版本", "连接类型", "账号", "状态"]
        self.iponeTbWidget.setColumnCount(len(self.header))
        self.iponeTbWidget.setHorizontalHeaderLabels(self.header)

        # 表宽度设置，用户可调整 QHeaderView.Custom, QHeaderView.Interactive
        self.iponeTbWidget.horizontalHeader().setDefaultSectionSize(100)
        self.iponeTbWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        # 表宽度自适应内容设置 QHeaderView.Stretch
        # self.iponeTbWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        # self.iponeTbWidget.itemClicked.connect(self.handleItemClicked)
        self.iponeTbWidget.setColumnWidth(0, 30)
        self.iponeTbWidget.setColumnWidth(1, 30)
        self.iponeTbWidget.setColumnWidth(2, 120)
        self.iponeTbWidget.setColumnWidth(3, 100)
        self.iponeTbWidget.setColumnWidth(4, 80)
        self.iponeTbWidget.setColumnWidth(5, 70)
        self.iponeTbWidget.setColumnWidth(6, 60)
        self.iponeTbWidget.setColumnWidth(7, 60)
        self.iponeTbWidget.setColumnWidth(8, 90)
        self.iponeTbWidget.setColumnWidth(9, 150)
        # 允许弹出菜单
        self.iponeTbWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        try:
            # 将信号请求连接到槽（单击鼠标右键，就调用方法）
            self.iponeTbWidget.customContextMenuRequested[QPoint].connect(self.rightMenuShow)
        except Exception as e:
            self.showLog("右键菜单异常:{}".format(e))

        # 按钮事件
        self.btnchklinks.clicked.connect(self.chkAllLinks)
        self.btnstart.clicked.connect(self.startRunAll)
        self.btnstop.clicked.connect(self.stopRunAll)
        #
        self.btnSelAll.clicked.connect(self.SelAll)
        self.btnRevSelAll.clicked.connect(self.RevSelAll)
        self.btnUnSelAll.clicked.connect(self.UnSelAll)
        #
        self.lbShellType.setText(define.CURTASKMODE)
        self.lbShellType.setStyleSheet("color:blue")
        self.labelver.setText("ver:20230105-1")


    # 没有用到
    def handleItemClicked(self, item):
        if item.checkState() == QtCore.Qt.Checked:
            # print('Checked')
            pass
        elif item.checkState() == QtCore.Qt.Unchecked:
            # print('Unchecked')
            pass

    # 全选
    def SelAll(self):
        for row in range(self.iponeTbWidget.rowCount()):
            if self.getRowUdid(row) is not None:
                if self.getRowChecked(row) == QtCore.Qt.Unchecked:
                    self.iponeTbWidget.item(row, 0).setCheckState(QtCore.Qt.Checked)

    # 反选
    def RevSelAll(self):
        for row in range(self.iponeTbWidget.rowCount()):
            if self.getRowUdid(row) is not None:
                if self.getRowChecked(row) == QtCore.Qt.Checked:
                    self.iponeTbWidget.item(row, 0).setCheckState(QtCore.Qt.Unchecked)
                else:
                    self.iponeTbWidget.item(row, 0).setCheckState(QtCore.Qt.Checked)

    # 全不选
    def UnSelAll(self):
        for row in range(self.iponeTbWidget.rowCount()):
            if self.getRowUdid(row) is not None:
                if self.getRowChecked(row) == QtCore.Qt.Checked:
                    self.iponeTbWidget.item(row, 0).setCheckState(QtCore.Qt.Unchecked)

    # 检测所有连接的iphone
    # 亮屏解锁后才能发现
    @log_exception
    def chkAllLinks(self, defvar=False):
        try:
            # 检测所有连接的iphone
            self.showLog("检测所有连接的iphone")
            res = CmdUtil.tidExec("tidevice list --json")  #
            # print(res)
            if res.find("[]") > -1 or res.find("market_name") > -1:
                listips = json.loads(res)
                if len(listips) > 0:
                    findcount = len(listips)
                    self.showLog("发现连接手机数量 {}".format(findcount))
                    #
                    needDeleteList = []  # 清空临时列表
                    newUdidList = []
                    for i in range(findcount):
                        # 清除多余的空格只保留一个
                        dicip = listips[i]
                        UDID = dicip["udid"]
                        SerialNumber = dicip["serial"]
                        NAME = dicip["name"]  # 如果这里又空格，将导致失败
                        MarketName = dicip["market_name"]
                        ProductVersion = dicip["product_version"]
                        ConnType = dicip["conn_type"]
                        Status = "等待"

                        #
                        newUdidList.append(UDID)
                        #
                        if UDID not in self.iphoneDict:
                            # 当前手机不在字典中，
                            self.iphoneDict[UDID] = {"UDID": UDID, "SerialNumber": SerialNumber, "NAME": NAME,
                                                     "MarketName": MarketName, "ProductVersion": ProductVersion,
                                                     "ConnType": ConnType, "Status": Status}
                    #
                    # 判断 self.iphoneDict中哪些手机需要删除
                    # 遍历
                    for key in self.iphoneDict.keys():
                        if len(newUdidList) > 0:
                            if key not in newUdidList:
                                needDeleteList.append(key)  # 需要删除的udid
                        else:
                            needDeleteList.append(key)  # 需要删除的udid
                    #
                    # 刷新表格界面
                    self.updateTabIPhones(needDeleteList)
                else:
                    QMessageBox().information(self, "提示", "未连接手机")
            else:
                self.showLog(res)
                # QMessageBox().information(self, "错误提示", res)
        except Exception as e:
            self.showLog("检测连接手机异常:{}".format(e))
            raise

    # 开启所有任务
    def startRunAll(self):
        try:
            for row in range(self.iponeTbWidget.rowCount()):
                if self.getRowUdid(row) is not None:
                    if self.iponeTbWidget.item(row, 0).checkState() == QtCore.Qt.Checked:
                        udid = self.getRowUdid(row).text()
                        # print(udid)
                        iphone = IPhoneInfo()  # 定义结构对象
                        iphone.RowIndex = row
                        iphone.RowNo = int(self.iponeTbWidget.item(row, 1).text())
                        iphone.UDID = udid
                        iphone.SerialNumber = self.iponeTbWidget.item(row, 3).text()
                        iphone.NAME = self.iponeTbWidget.item(row, 4).text()
                        iphone.MarketName = self.iponeTbWidget.item(row, 5).text()
                        iphone.ProductVersion = self.iponeTbWidget.item(row, 6).text()
                        iphone.ConnType = self.iponeTbWidget.item(row, 7).text()
                        # iphone.Status = self.iponeTbWidget.item(row, 9).text()
                        #
                        self.runTaskThread(iphone)
        except Exception as e:
            self.showLog("开启所有任务异常:{}".format(e))

    # 停止所有任务 没有用到
    def stopRunAll(self):
        # QMessageBox().information(None, "消息", "暂时没有", QMessageBox.Ok, QMessageBox.Ok)
        # 被子线程的信号触发，更新一次时间
        self.fmAutoTask.exec()  # 显示对话框--模态---阻塞
        self.lbShellType.setText(define.CURTASKMODE)
        self.lbShellType.setStyleSheet("color:blue")

    # 运行任务线程
    @log_exception
    def runTaskThread(self, iphone):
        try:
            if iphone.UDID not in self.taskDict:
                # 线程还没创建，就新建任务线程
                self.showLog("{} 号手机开始任务脚本".format(iphone.RowNo))
                iphone.State = 1

                if define.CURTASKMODE == TaskMode.wx自动注册.name:
                    thtask = wxAutoRegThread(iphone, define.PACKAGENAME, define.WDAPORT, define.CURTASKMODE)
                    # thtask.moveToThread(thtask)
                    # 将子线程中的信号与statusUpdate槽函数绑定
                    thtask.updateStatus.connect(self.statusUpdate)
                    thtask.updateLogs.connect(self.showLog)
                    #
                    thtask.start()

                    self.taskDict[iphone.UDID] = thtask  # 加入任务字典
                    # thtask.terminate() # 有效退出
                    # os.kill(thtask.PID, signal.SIGKILL) 导致整个软件退出

                elif define.CURTASKMODE == TaskMode.wx自动登录.name:
                    thtask = wxAutoLoginThread(iphone, define.PACKAGENAME, define.WDAPORT, define.CURTASKMODE)
                    # thtask.moveToThread(thtask)
                    # 将子线程中的信号与statusUpdate槽函数绑定
                    thtask.updateStatus.connect(self.statusUpdate)
                    thtask.updateLogs.connect(self.showLog)
                    #
                    thtask.start()

                    self.taskDict[iphone.UDID] = thtask  # 加入任务字典
                    # thtask.terminate() # 有效退出
                    # os.kill(thtask.PID, signal.SIGKILL) 导致整个软件退出
                else:
                    self.showStatus("不支持的脚本运行模式")

            else:
                if self.taskDict[iphone.UDID].isRunning():
                    self.showLog("{} 号手机 已经在运行".format(iphone.RowNo))
                    # self.taskDict[iphone.UDID].start()
                else:
                    self.showLog("{} 号手机 继续运行".format(iphone.RowNo))
                    self.taskDict[iphone.UDID].start()
        except Exception as e:
            self.showLog("运行任务异常:{}".format(e))

    # 更新运行状态
    def statusUpdate(self, rowno, rowindex, colindex, data):
        try:
            if self.iponeTbWidget.item(rowindex, colindex) is not None:
                self.iponeTbWidget.item(rowindex, colindex).setText(data)
            else:
                for row in range(self.iponeTbWidget.rowCount()):
                    if self.getRowUdid(row) is not None:
                        if self.getRowChecked(row) == QtCore.Qt.Checked:
                            if rowno == int(self.iponeTbWidget.item(row, 1).text()):
                                self.iponeTbWidget.item(row, colindex).setText(data)
                                break
        except Exception as e:
            self.showLog("更新运行状态异常:{}".format(e))

    # 右键菜单
    @log_exception
    def rightMenuShow(self, defval=""):
        try:
            # 得到索引
            rowNum = -1
            # for i in self.iponeTbWidget.selectionModel().selection().indexes():
            #     rowNum = i.row()
            if len(self.iponeTbWidget.selectionModel().selection().indexes()) > 0:
                rowNum = 1
            # 如果选择的行索引小于1，弹出上下文菜单
            if rowNum < 0:
                return

            if self.rightMenu is None:
                self.rightMenu = QMenu(self.iponeTbWidget)
                #
                startAction = QAction(u"运行脚本", self)  # , triggered=self.rowsRemove()
                startAction.triggered.connect(lambda: self.startTask())
                self.rightMenu.addAction(startAction)
                #
                gotoAction = QAction(u"继续运行脚本", self)  # , triggered=self.rowsRemove()
                gotoAction.triggered.connect(lambda: self.gotoTask())
                self.rightMenu.addAction(gotoAction)
                #
                self.rightMenu.addSeparator()
                #
                stopAction = QAction(u"停止运行脚本", self)  # , triggered=self.rowsRemove()
                stopAction.triggered.connect(lambda: self.stopSelTask())
                self.rightMenu.addAction(stopAction)
                #
                #
                redoAction = QAction(u"重置脚本", self)  # , triggered=self.rowsRemove()
                redoAction.triggered.connect(lambda: self.redoTask())
                self.rightMenu.addAction(redoAction)
                #
                redouserAction = QAction(u"重置脚本包括账号", self)  # , triggered=self.rowsRemove()
                redouserAction.triggered.connect(lambda: self.redoTaskUser())
                self.rightMenu.addAction(redouserAction)
                #
                self.rightMenu.addSeparator()
                #
                userlogAction = QAction(u"查看日志", self)
                userlogAction.triggered.connect(lambda: self.getUserLogs())
                self.rightMenu.addAction(userlogAction)
                self.rightMenu.addSeparator()
                #
                ###############################
                autotaskMenu = QMenu('批量自动任务', self)
                autotaskSetAction = QAction(u"配置自动任务", self)
                autotaskSetAction.triggered.connect(lambda: self.configAutoTask())
                autotaskMenu.addAction(autotaskSetAction)
                #
                autotaskRunAction = QAction(u"立即执行自动任务", self)
                autotaskRunAction.triggered.connect(lambda: self.runAutoTask())
                autotaskMenu.addAction(autotaskRunAction)
                #
                self.rightMenu.addMenu(autotaskMenu)
                ################################
                self.rightMenu.addSeparator()
                ###############################
                qicon = QIcon(define.STARTPATH + '/images/arrow_next.png')
                onetaskMenu = QMenu('单步执行任务', self)
                onetaskMenu.setIcon(qicon)
                for itemname in define.TASK_FULL:
                    onetaskAction = QAction(itemname, self)
                    onetaskAction.setCheckable(False)
                    onetaskAction.setChecked(False)
                    onetaskAction.setData("0")
                    # onetaskAction.data()
                    onetaskAction.setIcon(qicon)
                    # onetaskAction.isChecked()
                    onetaskAction.triggered.connect(functools.partial(self.runOneTask, onetaskAction, itemname))
                    onetaskMenu.addAction(onetaskAction)
                #
                self.rightMenu.addMenu(onetaskMenu)
                ################################

                self.rightMenu.addSeparator()

                #
                reinsAction = QAction(u"重装目标APP", self)
                reinsAction.triggered.connect(lambda: self.reinstallApp())
                self.rightMenu.addAction(reinsAction)
                #
                wdaAction = QAction(u"安装WDA", self)
                wdaAction.triggered.connect(lambda: self.installWDA())
                self.rightMenu.addAction(wdaAction)
                #
                self.rightMenu.addSeparator()
                #
                removeAction = QAction(u"删除连接", self)
                removeAction.triggered.connect(lambda: self.rowsRemove())
                self.rightMenu.addAction(removeAction)
                #
            #
            self.rightMenu.exec_(QCursor.pos())
        except Exception as e:
            self.showLog("右键菜单异常:{}".format(e))

    # 开始脚本
    def startTask(self):
        if len(self.iponeTbWidget.selectedItems()) > 0:
            dalog = QMessageBox().question(None, "询问", "确认开始脚本？", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if dalog == QMessageBox.Yes:
                try:
                    alist = []
                    for item in self.iponeTbWidget.selectedItems():
                        udid = self.getRowUdid(item.row()).text()
                        if self.iponeTbWidget.item(item.row(), 0).checkState() != QtCore.Qt.Checked:
                            QMessageBox().information(None, "消息", "没有勾选", QMessageBox.Ok, QMessageBox.Ok)
                        else:
                            if udid not in alist:
                                alist.append(udid)
                                row = item.row()
                                #
                                iphone = IPhoneInfo()  # 定义结构对象
                                iphone.RowIndex = row
                                iphone.RowNo = int(self.iponeTbWidget.item(row, 1).text())
                                iphone.UDID = udid
                                iphone.SerialNumber = self.iponeTbWidget.item(row, 3).text()
                                iphone.NAME = self.iponeTbWidget.item(row, 4).text()
                                iphone.MarketName = self.iponeTbWidget.item(row, 5).text()
                                iphone.ProductVersion = self.iponeTbWidget.item(row, 6).text()
                                iphone.ConnType = self.iponeTbWidget.item(row, 7).text()
                                # iphone.Status = self.iponeTbWidget.item(row, 9).text()
                                #

                                self.runTaskThread(iphone)
                except Exception as e:
                    self.showLog("开始脚本异常:{}".format(e))

    # 停止
    def stopTask(self):
        if len(self.iponeTbWidget.selectedItems()) > 0:
            dalog = QMessageBox().question(None, "询问", "确认停止？", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if dalog == QMessageBox.Yes:
                try:
                    alist = []
                    for item in self.iponeTbWidget.selectedItems():
                        udid = self.getRowUdid(item.row()).text()
                        if self.iponeTbWidget.item(item.row(), 0).checkState() != QtCore.Qt.Checked:
                            QMessageBox().information(None, "消息", "没有勾选", QMessageBox.Ok, QMessageBox.Ok)
                        else:
                            if udid not in alist:
                                alist.append(udid)
                                pass
                except Exception as e:
                    self.showLog("停止脚本异常:{}".format(e))

    # 继续脚本--选定行
    def gotoTask(self):
        if len(self.iponeTbWidget.selectedItems()) > 0:
            dalog = QMessageBox().question(None, "询问", "确认继续脚本？", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if dalog == QMessageBox.Yes:
                try:
                    alist = []
                    for item in self.iponeTbWidget.selectedItems():
                        udid = self.getRowUdid(item.row()).text()
                        if self.iponeTbWidget.item(item.row(), 0).checkState() != QtCore.Qt.Checked:
                            QMessageBox().information(None, "消息", "没有勾选", QMessageBox.Ok, QMessageBox.Ok)
                            break
                        else:
                            if udid not in alist:
                                alist.append(udid)
                                pass
                except Exception as e:
                    self.showLog("继续脚本异常:{}".format(e))

    # 停止运行脚本--选定行
    @log_exception
    def stopSelTask(self, defval=""):
        if len(self.iponeTbWidget.selectedItems()) > 0:
            dalog = QMessageBox().question(None, "询问", "确认停止运行脚本？", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if dalog == QMessageBox.Yes:
                try:
                    alist = []
                    for item in self.iponeTbWidget.selectedItems():
                        udid = self.getRowUdid(item.row()).text()
                        if self.iponeTbWidget.item(item.row(), 0).checkState() != QtCore.Qt.Checked:
                            QMessageBox().information(None, "消息", "没有勾选", QMessageBox.Ok, QMessageBox.Ok)
                            break
                        else:
                            if udid not in alist:
                                if udid in self.taskDict:
                                    # 清除单元格账号
                                    self.iponeTbWidget.item(item.row(), 9).setText("")
                                    # 清除步骤列表
                                    self.taskDict[udid].stopSelTask()
                                    self.taskDict[udid].terminate()  # 退出正在运行的线程
                                    #
                except Exception as e:
                    self.showLog("停止运行脚本异常:{}".format(e))

    # 重置脚本--选定行
    @log_exception
    def redoTask(self, defval=""):
        if len(self.iponeTbWidget.selectedItems()) > 0:
            dalog = QMessageBox().question(None, "询问", "确认重置脚本？", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if dalog == QMessageBox.Yes:
                try:
                    alist = []
                    for item in self.iponeTbWidget.selectedItems():
                        udid = self.getRowUdid(item.row()).text()
                        if self.iponeTbWidget.item(item.row(), 0).checkState() != QtCore.Qt.Checked:
                            QMessageBox().information(None, "消息", "没有勾选", QMessageBox.Ok, QMessageBox.Ok)
                            break
                        else:
                            if udid not in alist:
                                if udid in self.taskDict:
                                    # 清除单元格账号
                                    self.iponeTbWidget.item(item.row(), 9).setText("")
                                    # 清除步骤列表
                                    self.taskDict[udid].recoverySteps(ResetType.ResetScript)
                                    self.taskDict[udid].terminate()  # 退出正在运行的线程
                                    self.taskDict[udid].start()
                                    #
                except Exception as e:
                    self.showLog("重置脚本异常:{}".format(e))

    # 重置脚本和账号--选定行
    @log_exception
    def redoTaskUser(self, defval=""):
        if len(self.iponeTbWidget.selectedItems()) > 0:
            dalog = QMessageBox().question(None, "询问", "确认重置脚本和账号？", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if dalog == QMessageBox.Yes:
                try:
                    alist = []
                    for item in self.iponeTbWidget.selectedItems():
                        udid = self.getRowUdid(item.row()).text()
                        if self.iponeTbWidget.item(item.row(), 0).checkState() != QtCore.Qt.Checked:
                            QMessageBox().information(None, "消息", "没有勾选", QMessageBox.Ok, QMessageBox.Ok)
                            break
                        else:
                            if udid not in alist:
                                if udid in self.taskDict:
                                    # 清除单元格账号
                                    self.iponeTbWidget.item(item.row(), 8).setText("")
                                    self.iponeTbWidget.item(item.row(), 9).setText("")
                                    # 清除步骤列表
                                    self.taskDict[udid].recoverySteps(ResetType.ResetScriptUser)
                                    self.taskDict[udid].terminate()  # 退出正在运行的线程
                                    self.taskDict[udid].start()
                                    #
                except Exception as e:
                    self.showLog("重置脚本和账号异常:{}".format(e))

    # 删除选定行
    @log_exception
    def rowsRemove(self, defval=""):
        if len(self.iponeTbWidget.selectedItems()) > 0:
            dalog = QMessageBox().question(None, "询问", "确认删除？", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if dalog == QMessageBox.Yes:
                try:
                    alist = []
                    for item in self.iponeTbWidget.selectedItems():
                        udid = self.getRowUdid(item.row()).text()
                        if udid not in alist:
                            alist.append(udid)
                            #
                            self.showLog("移除 手机 {}".format(udid))
                            self.iphoneDict.pop(udid)
                            self.iponeTbWidget.removeRow(item.row())
                            if udid in self.taskDict:
                                #pid = self.taskDict[udid].PID
                                self.taskDict[udid].needStopOut()
                                self.taskDict[udid].terminate()  # 终止正在运行的线程
                                self.taskDict.pop(udid)  # 从字典中移除

                            #
                    #
                    self.labStatus.setText("当前状态：连接数 {}".format(self.iponeTbWidget.rowCount()))
                except Exception as e:
                    self.showLog("删除选定行异常:{}".format(e))

    # 设置自动任务
    def configAutoTask(self):
        self.fmAutoTask.show()

    def runOneTask(self, action, menutext):
        if menutext == ETASK.获取wxid.name:
            self.getUserWxid(action)
        elif menutext == ETASK.退出微信.name:
            self.logoutTask(action)
        else:
            self.showLog("不支持直接调用")

    #
    # 立即运行自动任务
    def runAutoTask(self):
        if len(self.iponeTbWidget.selectedItems()) > 0:
            dalog = QMessageBox().question(None, "询问", "确认立即运行自动任务？", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if dalog == QMessageBox.Yes:
                try:
                    alist = []
                    for item in self.iponeTbWidget.selectedItems():
                        udid = self.getRowUdid(item.row()).text()
                        if self.iponeTbWidget.item(item.row(), 0).checkState() != QtCore.Qt.Checked:
                            QMessageBox().information(None, "消息", "没有勾选", QMessageBox.Ok, QMessageBox.Ok)
                            break
                        else:
                            if udid not in alist:
                                if udid in self.taskDict and self.taskDict[udid].getLogined():
                                    #
                                    self.manualRunAutoTask(udid)
                                else:
                                    self.showLog("没有登录APP {}".format(udid))
                except Exception as e:
                    self.showLog("获取wxid异常:{}".format(e))

    def manualRunAutoTask(self, udid):
        # 创建线程
        bkTh = threading.Thread(target=self.taskDict[udid].manualRunAutoTask)
        bkTh.setDaemon(True)  # 设置为守护进程
        bkTh.start()

    # 获取用户日志
    def getUserLogs(self):
        try:
            alist = []
            for item in self.iponeTbWidget.selectedItems():
                udid = self.getRowUdid(item.row()).text()
                if udid not in alist:
                    wxuser = self.iponeTbWidget.item(item.row(), 8).text()
                    if wxuser is not None and wxuser != "":
                        curtime = time.strftime('%Y%m%d', time.localtime(time.time()))
                        fileName = define.STARTPATH + "/logs/{}_{}.log".format(curtime, wxuser.replace("+", ""))
                        self.showLog(fileName)
                        subprocess.call(['open', fileName])
                        #
        except Exception as e:
            self.showLog("获取用户日志异常:{}".format(e))


    # 退出WX APP
    def logoutTask(self, action=None):
        if len(self.iponeTbWidget.selectedItems()) > 0:
            dalog = QMessageBox().question(None, "询问", "确认退出账号？", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if dalog == QMessageBox.Yes:
                try:
                    alist = []
                    for item in self.iponeTbWidget.selectedItems():
                        udid = self.getRowUdid(item.row()).text()
                        if self.iponeTbWidget.item(item.row(), 0).checkState() != QtCore.Qt.Checked:
                            QMessageBox().information(None, "消息", "没有勾选", QMessageBox.Ok, QMessageBox.Ok)
                            break
                        else:
                            if udid not in alist:
                                if udid in self.taskDict and self.taskDict[udid].getLogined():
                                    # 清除步骤列表
                                    self.taskDict[udid].logoutAppInTreadNoJoin()
                                else:
                                    self.showLog(udid + " 没有登录APP {}".format(udid))
                except Exception as e:
                    self.showLog("退出APP异常:{}".format(e))
        # 重装APP

    # 重装目标APP
    def reinstallApp(self):
        if len(self.iponeTbWidget.selectedItems()) > 0:
            dalog = QMessageBox().question(None, "询问", "确认重装目标APP？", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if dalog == QMessageBox.Yes:
                try:
                    alist = []
                    for item in self.iponeTbWidget.selectedItems():
                        udid = self.getRowUdid(item.row()).text()
                        if self.iponeTbWidget.item(item.row(), 0).checkState() != QtCore.Qt.Checked:
                            QMessageBox().information(None, "消息", "没有勾选", QMessageBox.Ok, QMessageBox.Ok)
                            break
                        else:
                            if udid not in alist:
                                if udid in self.taskDict and self.taskDict[udid].getLogined():
                                    dalog = QMessageBox().question(None, "询问", "{} 已经登录，确认重装目标APP?".format(udid),
                                                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
                                    if dalog == QMessageBox.Yes:
                                        self.reinstallThread(udid)
                                else:
                                    self.reinstallThread(udid)

                except Exception as e:
                    self.showLog("重装目标APP异常:{}".format(e))

    # 重装APP
    def reinstallThread(self, udid):
        # 创建线程
        bkTh = threading.Thread(target=self.reInstallFunc, args=[udid])
        bkTh.setDaemon(True)  # 设置为守护进程
        bkTh.start()

    def reInstallFunc(self, udid):
        try:
            self.showLog(udid + " 卸载目标APP...")
            uninstallTargetApp(udid, define.PACKAGENAME, self.showLog)
            self.showLog(udid + " 安装目标APP...")
            installTargetApp(udid, define.THEIPAFILE, self.showLog)
        except Exception as e:
            self.showLog(udid + " 重装APP异常:{}".format(e))


    def installWDA(self):
        if len(self.iponeTbWidget.selectedItems()) > 0:
            dalog = QMessageBox().question(None, "询问", "确认重装WDA？", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if dalog == QMessageBox.Yes:
                try:
                    alist = []
                    for item in self.iponeTbWidget.selectedItems():
                        udid = self.getRowUdid(item.row()).text()
                        if self.iponeTbWidget.item(item.row(), 0).checkState() != QtCore.Qt.Checked:
                            QMessageBox().information(None, "消息", "没有勾选", QMessageBox.Ok, QMessageBox.Ok)
                            break
                        else:
                            if udid not in alist:
                                self.reinstallOtherThread(udid, "{}/res/wda.ipa".format(define.STARTPATH))

                except Exception as e:
                    self.showLog(udid + " 重装WDA异常:{}".format(e))


    # 更新iphone列表界面
    def updateTabIPhones(self, needDeleteList):
        self.showLog("更新iphone列表界面")
        # 删除所有失去连接的手机
        self.deleteUnlinkIPhoe(needDeleteList)
        #
        for key in self.iphoneDict:
            # UDID  SerialNumber    NAME        MarketName    ProductVersion    ConnType
            if self.gridExistUDID(key) is False:
                try:
                    # 还不存在,新手机插入到最前面
                    # self.iponeTbWidget.insertRow(line)
                    line = self.iponeTbWidget.rowCount()  # 返回当前行数（尾部）
                    self.iponeTbWidget.insertRow(line)
                    chkBoxItem = QTableWidgetItem()
                    chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                    chkBoxItem.setCheckState(QtCore.Qt.Unchecked)

                    # table.setItem(rowNo, 9, chkBoxItem)
                    self.iponeTbWidget.setItem(line, 0, chkBoxItem)
                    self.iponeTbWidget.setItem(line, 1, QTableWidgetItem(str(self.rowNo)))
                    self.iponeTbWidget.setItem(line, 2, QTableWidgetItem(key))
                    self.iponeTbWidget.setItem(line, 3, QTableWidgetItem(self.iphoneDict[key]["SerialNumber"]))
                    self.iponeTbWidget.setItem(line, 4, QTableWidgetItem(self.iphoneDict[key]["NAME"]))
                    self.iponeTbWidget.setItem(line, 5, QTableWidgetItem(self.iphoneDict[key]["MarketName"]))
                    self.iponeTbWidget.setItem(line, 6, QTableWidgetItem(self.iphoneDict[key]["ProductVersion"]))
                    self.iponeTbWidget.setItem(line, 7, QTableWidgetItem(self.iphoneDict[key]["ConnType"]))
                    self.iponeTbWidget.setItem(line, 8, QTableWidgetItem(""))
                    self.iponeTbWidget.setItem(line, 9, QTableWidgetItem(self.iphoneDict[key]["Status"]))
                    # 累加行号
                    self.rowNo += 1
                    # 禁止编辑单元格
                    for j in range(len(self.header)):
                        cell_item = self.iponeTbWidget.item(line, j)
                        cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)

                    #
                    self.showLog("新增 手机 {}".format(key))
                except Exception as e:
                    self.showLog("新增手机异常:{}".format(e))

        #
        line = self.iponeTbWidget.rowCount()  # 返回当前行数（尾部）
        self.labStatus.setText("当前状态：连接数 {}".format(line))

    # 判断表格中是否已经存在 udid
    def gridExistUDID(self, udid):
        try:
            for row in range(self.iponeTbWidget.rowCount()):
                if self.getRowUdid(row) is not None:
                    curudid = self.getRowUdid(row).text()
                    if curudid == udid:
                        return True
            #
        except Exception as e:
            self.showLog("判断udid异常:{}".format(e))
        return False

    # 获取指定行的UDID
    def getRowUdid(self, rowindex):
        try:
            return self.iponeTbWidget.item(rowindex, 2)
        except Exception as e:
            self.showLog("获取udid异常:{}".format(e))
        return None

    # 获取指定行的勾选状态
    def getRowChecked(self, rowindex):
        try:
            return self.iponeTbWidget.item(rowindex, 0).checkState()
        except Exception as e:
            self.showLog("获取勾选状态异常:{}".format(e))
        return QtCore.Qt.Unchecked

    # 删除所有失去连接的手机
    @log_exception
    def deleteUnlinkIPhoe(self, needDeleteList):
        if len(needDeleteList) > 0:
            try:
                self.showLog("删除所有失去连接的手机")
                for irow in range(len(needDeleteList)):
                    udid1 = needDeleteList[irow]
                    max = self.iponeTbWidget.rowCount()
                    i = 0
                    while i < max:
                        if self.getRowUdid(i) is not None:
                            udid2 = self.getRowUdid(i).text()
                            if udid2 == udid1:
                                # 移除任务字典
                                if udid2 in self.taskDict:
                                    pid = self.taskDict[udid2].PID
                                    self.taskDict[udid2].needStopOut()
                                    self.taskDict[udid2].terminate()  # 退出正在运行的线程
                                    self.taskDict.pop(udid2)  # 从字典中移除
                                    #

                                # 移除手机字典
                                self.iphoneDict.pop(udid2)
                                # 移除表格行
                                self.iponeTbWidget.removeRow(i)  # 移除当前行
                                max = self.iponeTbWidget.rowCount()  # 重新计算行数
                                self.showLog("移除 手机 {}".format(udid2))
                                continue
                        #
                        i += 1
            except Exception as e:
                self.showLog("删除失连手机异常:{}".format(e))

    # 清除所有手机 目前没有调用
    def clearAllLinkIPhone(self):
        self.iponeTbWidget.setRowCount(0)
        self.iponeTbWidget.clearContents()

    #
    def refreshChecks(self):
        pass

    # 打印操作日志
    def showLog(self, logstr):
        try:
            if self.txtoutLogs.blockCount() > 200:
                # 清空日志
                self.txtoutLogs.setPlainText("")
            #
            datestr = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S   ')
            self.txtoutLogs.appendPlainText(datestr + logstr)
        except Exception as e:
            print("保存到日志文件异常:{}".format(e))
