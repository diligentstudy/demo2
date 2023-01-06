from entitys import define
from entitys.eLanguage import enumLanguage as LANG
import time

# eExpression

# 点击坐标
from common import CmdUtil


def clickCoordinate(client, tkey, model=""):
    try:
        if model == "":
            model = define.DEFMOBILEMODEL
        #
        s = tkey.M(model)
        # p = tuple(eval("(%s)" % s)) #字符串转为元组，返回：(1,3)
        ps = s.split(",")
        x = float(ps[0])
        y = float(ps[1])
        client.click(x, y)
    except Exception as e:
        pass


def getpreNameEqual(text):
    return 'name == "{}"'.format(text)


def getpreLabelEqual(text):
    return 'label == "{}"'.format(text)


def getpreNameContains(text):
    return 'name CONTAINS "{}"'.format(text)


def getpreLabelContains(text):
    return 'label CONTAINS "{}"'.format(text)


# 设置目标APP为前置活动应用
def getCurrentApp(client, showLog):
    try:
        #
        if client.app_current is not None:
            boundleid = client.app_current()["bundleId"]
            showLog("getCurrentApp: " + boundleid)
            if boundleid == define.PACKAGENAME:
                return True
            elif boundleid == "com.apple.springboard":
                # 弹窗1
                # 微信 该ID因涉嫌滥用已被屏蔽。 要继续使用此帐户，请点击“同意”并在“限制”部分请求删除。
                # 取消 同意
                if client(name=LANG.取消.T()).exists:
                    client(name=LANG.取消.T()).click()
                if client(className="XCUIElementTypeButton", name=LANG.关掉.T()).exists:
                    showLog("点击浮动弹窗")
                    client(name=LANG.关掉.T()).click
                # if client(className="XCUIElementTypeStaticText", name=LANG.信任弹窗.T()).exists:
                #     showLog("点击信任弹框")
                #     client(name=LANG.允许.T()).click
        else:
            showLog("getCurrentApp is None")

    except Exception as e:
        showLog("setCurrentApp 异常：{}".format(e))
    #
    return False


# 设置目标APP为前置活动应用
def setCurrentApp(client, udid, showLog):
    try:
        showLog("setCurrentApp")
        # if client.app_current is not None:
        #     ##{'processArguments': {'env': {}, 'args': []}, 'name': '', 'pid': 4884, 'bundleId': 'com.tencet.xin001'}
        #     if client.app_current()["bundleId"] != define.PACKAGENAME:
        #         client.app_launch(define.PACKAGENAME)
        #
        tres = CmdUtil.exec2("tidevice --udid {} launch {}".format(udid,define.PACKAGENAME))
        if tres is not None and tres.find("None") == -1:
            showLog(tres)  # None
    except Exception as e:
        showLog("setCurrentApp 异常：{}".format(e))


# 主导航_聊天
def clickBarTalk(client):
    clickCoordinate(client, LANG.主导航_聊天)


# 主导航_通讯录
def clickBarContact(client):
    clickCoordinate(client, LANG.主导航_通讯录)


# 主导航_发现
def clickBarFind(client):
    clickCoordinate(client, LANG.主导航_发现)


# 主导航_我
def clickBarMe(client):
    clickCoordinate(client, LANG.主导航_我)


# 关闭 左上角左箭头返回按钮
# 关闭 左上角关闭按钮
# 关闭 右上角取消按钮
# 返回wx主界面
def gobakMain(client, showLog):
    try:
        showLog("返回APP主界面")
        while True:
            cnt = 0
            if client(label=LANG.左上角左箭头返回.T()).exists:
                cnt += 1
                showLog("点击 左上角左箭头返回")
                clickCoordinate(client, LANG.左上角左箭头返回)
                # time.sleep(1)

            if client(name=LANG.关闭.T()).exists:
                cnt += 1
                showLog("点击 关闭")
                client(name=LANG.关闭.T()).click()
                # time.sleep(1)

            if client(className="XCUIElementTypeStaticText", name=LANG.POPF选择登录方式.T()).exists:
                cnt += 1
                showLog("点击 选择登录方式_关闭")
                clickCoordinate(client, LANG.POPF选择登录方式_关闭)

            if client(name=LANG.取消.T()).exists:
                cnt += 1
                showLog("点击 取消")
                client(name=LANG.取消.T()).click()
                # time.sleep(1)
            #
            if cnt == 0:
                # 没有任何可以点的，就退出
                return
    except Exception as e:
        pass


# 左上角左箭头返回
def leftArrowBack(client, times=0):
    try:
        i = 0
        waitsou = 'label CONTAINS "{}"'.format(LANG.左上角左箭头返回.T())
        while True:
            # 左上角左箭头返回
            jtou = client(className="XCUIElementTypeButton", label=LANG.左上角左箭头返回.T())
            if jtou.exists:
                # jtou.click()
                clickCoordinate(client, LANG.左上角左箭头返回)
                # time.sleep(1)
                if times > 0:
                    i += 1
                    if i >= times:
                        return
            # ย้อนกลับ,1 左上角左箭头返回 后面有消息的数量，再聊天窗口有出息
            elif client(predicate=waitsou).exists:
                # client(predicate=waitsou, index=1).click()
                clickCoordinate(client, LANG.左上角左箭头返回)
                # time.sleep(1)
                if times > 0:
                    i += 1
                    if i >= times:
                        return
            else:
                return

    except Exception as e:
        print("leftArrowBack 异常 {}".format(e))


# 左上角关闭按钮
def leftCloseBtn(client, times=0):
    i = 0
    while True:
        if client(label=LANG.关闭.T()).exists:
            client(label=LANG.关闭.T()).click()
            # time.sleep(1)
            if times > 0:
                i += 1
                if i >= times:
                    return
        else:
            return


# 关闭不在显示弹窗
def clickDontShowAgain(client):
    try:
        if client(name=LANG.不再显示.T()).exists:
            client(name=LANG.不再显示.T()).click()
    except Exception as e:
        pass


# label值如果存在就点击
def click_Exists(client, tkey, timeout=30):
    try:
        lb = tkey.T()
        # #client(predicate=getpreLabelEqual(lb)).click_exists(timeout)
        # client(label=lb).click_exists(timeout)
        click_common(client, tkey)
    except Exception as e:
        pass


def click_common(client, tkey):
    try:
        lb = tkey.T()
        # client(predicate=getpreLabelEqual(lb)).click_exists(timeout)
        client(label=lb).click()
    except Exception as e:
        pass


# 输入文字到 TextField
def enterText_Exists(client, text, index=1):
    try:
        if index <= 1:
            tf = client(className='XCUIElementTypeTextField')
        else:
            tf = client(className='XCUIElementTypeTextField', index=index)

        if tf.exists:
            tf.click()
            tf.clear_text()
            tf.set_text(text)
    except Exception as e:
        pass


def enterSecureText_Exists(client, text, index=1):
    try:
        if index <= 1:
            tf = client(className='XCUIElementTypeSecureTextField')
        else:
            tf = client(className='XCUIElementTypeSecureTextField', index=index)

        if tf.exists:
            tf.click()
            tf.clear_text()
            tf.set_text(text)
    except Exception as e:
        pass


# 输入文字到 TextView
def enterTextView_Exists(client, text, index=1):
    try:
        if index <= 1:
            tf = client(className='XCUIElementTypeTextView')
        else:
            tf = client(className='XCUIElementTypeTextView', index=index)
        if tf.exists:
            tf.click()
            tf.clear_text()
            tf.set_text(text)
    except Exception as e:
        pass


# 输入文字到 SearchField
def enterSearch_Exists(client, text, index=1):
    try:
        # client(className='XCUIElementTypeSearchField', index=index).set_text(text)
        if index <= 1:
            tf = client(className='XCUIElementTypeSearchField')
        else:
            tf = client(className='XCUIElementTypeSearchField', index=index)

        if tf.exists:
            tf.click()
            tf.clear_text()
            tf.set_text(text)
    except Exception as e:
        pass


# 获取文本
def getText_Exists(client, tkey):
    try:
        lb = tkey.T()
        return client(name=lb).text
    except Exception as e:
        pass


# 通过xpath 清空后输入内容
def clear_set_byxpath(client, strxpath, content):
    try:
        if client(xpath=strxpath).exists:
            tf = client(xpath=strxpath)
            tf.click()
            tf.clear_text()
            tf.set_text(content)
    except Exception as e:
        pass


# 通label 清空后输入内容
def clear_set_bylabel(client, label, content):
    try:
        if client(label=label).exists:
            txt = client(label=label)
            txt.click()
            txt.clear_text()
            txt.set_text(content)
    except Exception as e:
        pass


# 通过xpath 点击按钮或者标签
def clickButtonByXpath(client, strxpath):
    try:
        if client(xpath=strxpath).exists:
            client(xpath=strxpath).click()
    except Exception as e:
        pass
