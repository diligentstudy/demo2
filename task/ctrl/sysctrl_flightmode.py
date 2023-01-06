
#  切换飞行模式
import time

from common.ExLogHelper import log_exception


def switchFlightMode(client,showLog):
    showLog("...切换飞行模式...")
    times = 2
    for i in range(times):
        try:
            # 启动 设置
            client.app_launch('com.apple.Preferences')
            #
            client.xpath('//Switch').wait(5)
            if client.xpath('//Switch').value == "0":
                showLog("开启飞行模式")
                client.xpath('//Switch').click()  # 打开飞行模式
                time.sleep(0.5)
            if client.xpath('//Switch').value == "1":
                showLog("开启飞行模式-成功")

            if client.xpath('//Switch').value == "1":
                showLog("关闭飞行模式")
                client.xpath('//Switch').click()  # 关闭飞行模式
                time.sleep(0.5)
                if client.xpath('//Switch').value == "0":
                    showLog("关闭飞行模式-成功")
                    break
        except Exception as e:
            showLog("切换飞行模式 异常:{}".format(e))

    client.app_terminate('com.apple.Preferences')

#  打开飞行模式
@log_exception
def openFlightMode(client,showLog):
    times = 2
    for i in range(times):
        try:
            # 启动 设置
            client.app_launch('com.apple.Preferences')
            #
            client.xpath('//Switch').wait(5)
            if client.xpath('//Switch').value == "0":
                showLog("开启飞行模式")
                client.xpath('//Switch').click()  # 打开飞行模式
                time.sleep(0.5)
            if client.xpath('//Switch').value == "1":
                showLog("开启飞行模式-成功")
                client.app_terminate('com.apple.Preferences')
                return True
        except Exception as e:
            showLog("打开飞行模式 异常:{}".format(e))
        #
        time.sleep(1)
    #
    client.app_terminate('com.apple.Preferences')
    return False

#  关闭飞行模式
@log_exception
def closeFlightMode(client,showLog):
    times = 2
    for i in range(times):
        try:
            # 启动 设置
            client.app_launch('com.apple.Preferences')
            #
            if client.xpath('//Switch').value == "1":
                showLog("关闭飞行模式")
                client.xpath('//Switch').click()  # 关闭飞行模式
                time.sleep(0.5)
            if client.xpath('//Switch').value == "0":
                showLog("关闭飞行模式-成功")
                client.app_terminate('com.apple.Preferences')
                return True
        except Exception as e:
            showLog("关闭飞行模式 异常:{}".format(e))
        #
        time.sleep(1)
    #
    client.app_terminate('com.apple.Preferences')
    return False
