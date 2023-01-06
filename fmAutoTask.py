import configparser
import os

from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QMessageBox, QListWidgetItem

from entitys import define
from ui.autotaskUI import Ui_Dialog


class FmAutoTask(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(FmAutoTask, self).__init__(parent)
        self.setupUi(self)
        self.setWindowOpacity(0.93)
        #
        # self.chkboxswg.clicked.connect(self.swg)

        self.btnup.clicked.connect(self.up)
        self.btndown.clicked.connect(self.down)
        self.btnclear.clicked.connect(self.clearList)

        self.btnsubmit.clicked.connect(self.submit)
        self.btncancle.clicked.connect(self.cancle)

        self.listfull.itemClicked.connect(self.clickedItemEvent)
        self.listfull.itemDoubleClicked.connect(self.doubleClickedItemEvent)

        self.listsel.itemDoubleClicked.connect(self.doubleClickedItemEvent_sel)

        self.cmbboxTaskType.currentIndexChanged.connect(self.currentIndex_Changed)  # 当选择内容改变时触发事件

        self.inifile = define.STARTPATH + '/config.ini'
        self.configINI = configparser.ConfigParser()  # configINI.readfp(open('config.ini',mode="r",encoding="utf-8"))
        self.configINI.read_file(open(self.inifile, mode="r", encoding="utf-8"))

        self.initData()

    def currentIndex_Changed(self):
        if self.cmbboxTaskType.currentIndex()>-1:
            seltxt = self.cmbboxTaskType.currentText()  # 获得当前内容
            #print(seltxt)

    def clickedItemEvent(self, item):
        name = item.text()
        # print("clicked", name)
        selitems = self.listsel.findItems(name, QtCore.Qt.MatchExactly)
        if selitems is not None and len(selitems) > 0:
            self.listsel.setCurrentItem(selitems[0])
        else:
            self.listsel.setCurrentItem(None)

    def doubleClickedItemEvent(self, item):
        name = item.text()
        # print("double clicked", name)
        selitems = self.listsel.findItems(name, QtCore.Qt.MatchExactly)
        if selitems is not None and len(selitems) > 0:
            self.listsel.setCurrentItem(selitems[0])
        else:
            self.listsel.addItem(name)

    def doubleClickedItemEvent_sel(self, item):
        self.listsel.takeItem(self.listsel.row(item))

    def initData(self):
        # 自动任务设置
        # 目前支持的自动任务类型：
        fulltask = self.configINI.get("autotask", "fulltask").split(",")
        # 当前配置的任务
        curlist = self.configINI.get("autotask", "curlist").split(",")
        #
        fulltaskmode = self.configINI.get("setting", "fulltaskmode").split(",")
        curtaskmode = self.configINI.get("setting", "curtaskmode")
        mobilemsg_ip = self.configINI.get("server", "mobilemsg_ip")
        hostserver = self.configINI.get("server", "hostserver")
        testuser = self.configINI.get("setting", "testuser")
        #
        ipafile = self.configINI.get("install", "ipafile")

        #
        self.cmbboxTaskType.addItems(fulltaskmode)
        self.editSmsServer.setText(mobilemsg_ip)
        self.editHkUserServer.setText(hostserver)
        self.editTestUser.setText(testuser)
        #
        self.editappfile.setText(ipafile)

        if curtaskmode != "":
            ps = fulltaskmode.index(curtaskmode)
            if ps > -1:
                self.cmbboxTaskType.setCurrentIndex(ps)  # 设置默认值
        #
        # self.cmbboxTaskType.setCurrentIndex
        # self.cmbboxTaskType.currentText()  # 获得当前内容

        if self.configINI.get("install", "reinstall") == "0":
            reinstall = False
        else:
            reinstall = True

        # 任务运行开关，0 不开启，1 开启
        if self.configINI.get("autotask", "runswg") == "0":
            runswg = False
        else:
            runswg = True
        #
        #
        if self.configINI.get("setting", "mustrelogin") == "0":
            mustrelogin = False
        else:
            mustrelogin = True
        #
        #
        if self.configINI.get("setting", "mustreimgbak") == "0":
            mustreimgbak = False
        else:
            mustreimgbak = True

        if self.configINI.get("setting", "fightmode") == "0":
            fightmode = False
        else:
            fightmode = True
        #
        if self.configINI.get("dragimage", "allowautodrag") == "0":
            allowautodrag = False
        else:
            allowautodrag = True


        #print(cv2.__file__)
        #print(sys.version)
        self.lbMsg.setText(self.configINI.get("autotask", "remark"))
        #
        self.chkboxswg.setChecked(runswg)
        self.chkboxrelogin.setChecked(mustrelogin)
        self.chkboxreimgbak.setChecked(mustreimgbak)
        self.chkboxreinstall.setChecked(reinstall)
        self.chkboxfight.setChecked(fightmode)
        self.chkboxautodrag.setChecked(allowautodrag) #  if self.configINI.get("dragimage", "allowautodrag"):
        #
        for i in fulltask:
            self.listfull.addItem(i)

        for i in curlist:
            self.listsel.addItem(i)

        self.lineEdit_login.setText(self.configINI.get("sjk", "login"))
        self.lineEdit_login_report.setText(self.configINI.get("sjk", "login_report"))
        self.lineEdit_reg.setText(self.configINI.get("sjk", "reg"))
        self.lineEdit_reg_report.setText(self.configINI.get("sjk", "reg_report"))
        self.lineEdit_reg_up_qrcode.setText(self.configINI.get("sjk", "reg_up_qrcode"))
        self.lineEdit_reportneedfriend.setText(self.configINI.get("sjk", "reportneedfriend"))

    # def swg(self):
    #     define.TASK_RUNSWG = self.chkboxswg.isChecked()

    def up(self):
        cidex = self.listsel.currentRow()
        if cidex < 0:
            QMessageBox().information(self, "提示", "请先选中一个项目")
            return
        if cidex == 0:
            QMessageBox().information(self, "提示", "已经到顶了")
            return
        cname = self.listsel.currentItem().text()
        #
        sels = []
        for i in range(self.listsel.count()):
            sels.append(self.listsel.item(i).text())
        #
        sels.remove(cname)
        sels.insert(cidex - 1, cname)
        #
        self.listsel.clear()
        for i in range(len(sels)):
            self.listsel.addItem(sels[i])
        #
        selitems = self.listsel.findItems(cname, QtCore.Qt.MatchExactly)
        if selitems is not None and len(selitems) > 0:
            self.listsel.setCurrentItem(selitems[0])
        else:
            self.listsel.setCurrentItem(None)

    def down(self):
        cidex = self.listsel.currentRow()
        if cidex < 0:
            QMessageBox().information(self, "提示", "请先选中一个项目")
            return
        if cidex == self.listsel.count() - 1:
            QMessageBox().information(self, "提示", "已经到底了")
            return
        cname = self.listsel.currentItem().text()
        #
        sels = []
        for i in range(self.listsel.count()):
            sels.append(self.listsel.item(i).text())
        #
        sels.remove(cname)
        sels.insert(cidex + 1, cname)
        #
        self.listsel.clear()
        for i in range(len(sels)):
            self.listsel.addItem(sels[i])
        #
        selitems = self.listsel.findItems(cname, QtCore.Qt.MatchExactly)
        if selitems is not None and len(selitems) > 0:
            self.listsel.setCurrentItem(selitems[0])
        else:
            self.listsel.setCurrentItem(None)

    def clearList(self):
        dalog = QMessageBox().question(None, "询问", "确认要清空已选用列表吗？", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if dalog == QMessageBox.Yes:
            self.listsel.clear()

    def cancle(self):
        self.close()

    def submit(self):
        try:
            #
            if self.editSmsServer.text() != "":
                if self.editSmsServer.text()[0:4] == "http":
                    QMessageBox().information(self, "提示", "短信服务器不能以http开头")
                    return
            if self.editHkUserServer.text() != "":
                if self.editHkUserServer.text()[0:4] != "http":
                    QMessageBox().information(self, "提示", "主服务器必须以http开头")
                    return
            if self.editTestUser.text() != "":
                if self.editTestUser.text().find("----") == -1:
                    QMessageBox().information(self, "提示", "测试账号格式不对")
                    return
            if self.chkboxreinstall.isChecked() and self.editappfile.text() == "":
                QMessageBox().information(self, "提示", "设置了重装APP必须填写APP路径")
                return

            if self.editappfile.text() == "":
                if os.path.exists(self.editappfile.text()) is False:
                    QMessageBox().information(self, "提示", "APP路径指向的文件不存在")
                    return

            sels = []
            for i in range(self.listsel.count()):
                # print(self.listsel.item(i).text())
                sels.append(self.listsel.item(i).text())
            #
            if len(sels) == 0:
                QMessageBox().information(self, "提示", "获取wxid 必须要有")
                return

            if sels[0] != "获取wxid":
                QMessageBox().information(self, "提示", "获取wxid 必须是第一个")
                return

            define.TASK_RUNSWG = self.chkboxswg.isChecked()
            define.MUSTRELOGIN = self.chkboxrelogin.isChecked()
            define.MUSTREIMGBAK = self.chkboxreimgbak.isChecked()
            define.NEEDREINSTALL = self.chkboxreinstall.isChecked()
            define.FIGHTMODESWG= self.chkboxfight.isChecked()
            define.ALLOWAUTODRAG = self.chkboxautodrag.isChecked()

            define.TASK_CURSET = sels

            if len(sels) > 0:
                self.configINI.set("autotask", "curlist", ','.join(sels))
            else:
                define.TASK_RUNSWG = False
                self.configINI.set("autotask", "curlist", "")
            #
            if define.TASK_RUNSWG:
                self.configINI.set("autotask", "runswg", "1")
            else:
                self.configINI.set("autotask", "runswg", "0")
            #
            if define.MUSTRELOGIN:
                self.configINI.set("setting", "mustrelogin", "1")
            else:
                self.configINI.set("setting", "mustrelogin", "0")
            #
            if define.MUSTREIMGBAK:
                self.configINI.set("setting", "mustreimgbak", "1")
            else:
                self.configINI.set("setting", "mustreimgbak", "0")
            #
            if define.NEEDREINSTALL:
                self.configINI.set("install", "reinstall", "1")
            else:
                self.configINI.set("install", "reinstall", "0")
            #
            if define.FIGHTMODESWG:
                self.configINI.set("setting", "fightmode", "1")
            else:
                self.configINI.set("setting", "fightmode", "0")
            #
            if define.ALLOWAUTODRAG: # if self.configINI.get("dragimage", "allowautodrag"):
                self.configINI.set("dragimage", "allowautodrag", "1")
            else:
                self.configINI.set("dragimage", "allowautodrag", "0")

            define.MOBILEMSG_IP = self.editSmsServer.text()
            define.HOSTSERVER = self.editHkUserServer.text()
            define.CURTASKMODE = self.cmbboxTaskType.currentText()
            define.TESTUSER = self.editTestUser.text()

            define.SJK_LOGIN = self.lineEdit_login.text()
            define.SJK_LOGIN_REPORT = self.lineEdit_login_report.text()
            define.SJK_REG = self.lineEdit_reg.text()
            define.SJK_REG_REPORT = self.lineEdit_reg_report.text()
            define.SJK_REG_UP_QRCODE = self.lineEdit_reg_up_qrcode.text()
            define.SJK_REPORT_NEEDFRIEND = self.lineEdit_reportneedfriend.text()

            self.configINI.set("sjk", "login",define.SJK_LOGIN)
            self.configINI.set("sjk", "login_report",define.SJK_LOGIN_REPORT)
            self.configINI.set("sjk", "reg", define.SJK_REG )
            self.configINI.set("sjk", "reg_report",define.SJK_REG_REPORT )
            self.configINI.set("sjk", "reg_up_qrcode", define.SJK_REG_UP_QRCODE )
            self.configINI.set("sjk", "reportneedfriend",define.SJK_REPORT_NEEDFRIEND )
            #
            self.configINI.set("server", "mobilemsg_ip", define.MOBILEMSG_IP)
            self.configINI.set("server", "hostserver", define.HOSTSERVER)
            self.configINI.set("setting", "curtaskmode", define.CURTASKMODE)
            self.configINI.set("setting", "testuser", define.TESTUSER)
            #
            self.configINI.set("install", "ipafile", self.editappfile.text())

            define.THEIPAFILE = "{}/res/{}".format(define.STARTPATH, self.editappfile.text())


            # self.cmbboxTaskType.setCurrentIndex
            # self.cmbboxTaskType.currentText()  # 获得当前内容

            # 把所作的修改写入配置文件
            with open(self.inifile, 'w', encoding='utf-8') as configfile:
                self.configINI.write(configfile)
            #
            QMessageBox().information(self, "提示", "保存配置成功")
            self.close()
        except Exception as e:
            QMessageBox().information(self, "提示","保存配置异常:{}".format(e.args[0]))
