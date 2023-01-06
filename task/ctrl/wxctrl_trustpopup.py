
from entitys import define
from entitys.eLanguage import enumLanguage as LANG

#点击信任弹框
def trustPopup(client, showLog):
    if client(name=LANG.信任弹窗.T()).exists:
        showLog("点击信任弹框")
        client(name=LANG.允许.T()).click