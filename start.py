import os
import sys

from PyQt5.QtWidgets import QApplication
import fmMain
# import uiautomator2 as u2
from entitys import define

if __name__ == '__main__':
    # 借助dirname()从绝对路径中提取目录
    current_file = os.path.abspath(sys.argv[0])
    define.STARTPATH = os.path.dirname(current_file)
    # sys.executable 当前的Python解释器路径
    define.EXECUTABLE = sys.executable # "/usr/bin/python"
    # print(os.getcwd())
    #
    myApp = QApplication(sys.argv)
    xmain = fmMain.xmainForm()
    # 设置图标
    # xmain.setWindowIcon(QIcon(startpath+'/images/logo1.png'))
    # ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("PyinstallerGUI")
    xmain.show()
    sys.exit(myApp.exec_())

