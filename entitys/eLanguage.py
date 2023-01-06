# 导入枚举类
from enum import Enum, unique
from entitys import define


# 多语言支持
class enumLanguage(Enum):

    确定 = {"cn": "确定", "en": "ok"}
    同意 = {"cn":"同意", "en": ""}
    取消 = {"cn": "取消", "en": ""}
    登录 = {"cn": "登录", "en": "login"}
    返回 = {"cn": "返回", "en": ""}
    提交 = {"cn": "返回", "en": ""}
    完毕 = {"cn": "完毕", "en": ""}
    结束 = {"cn": "结束", "en": ""}

    安全模式 = {"cn": "安全模式", "en": ""}
    无法重启客户端 = {"cn": "无法重启客户端", "en": ""}
    信任弹窗 = {"cn": "信任", "en": ""}
    允许 = {"cn": "允许", "en": ""}
    不允许 = {"cn": "允许", "en": ""}

    UI地球首页_登录 = {"cn": "登录", "en": "login"}
    UI地球首页_注册 = {"cn": "注册", "en": "reg"}

    微信团队 = {"cn": "微信团队", "en": ""}

    微信ID = {"cn": "微信ID", "en": "WeChat ID"}

    POP网络未连接= {"cn": "网络未连接稍后再试", "en": ""}
    POP按钮_同意= {"cn":"同意", "en": ""}

    POP联系失败检查网络设置 = {"cn": "用微信号/QQ号/邮箱登录", "en": ""}

    POPF选择登录方式={"cn": "选择登录方式", "en": ""}
    POPF选择登录方式_关闭 = {"cn": "关闭", "en": ""}

    ### UI窗口 ############################################
    UI默认无标题登录_通过短信验证码登录 = {"cn": "通过短信验证码登录", "en": ""}
    UI默认无标题登录_通过密码登录 = {"cn": "通过密码登录", "en": ""}
    UI默认无标题登录_登录 = {"cn": "登录", "en": "login"}
    UI默认无标题登录_更多选择 = {"cn": "更多选择", "en": ""}
    UI默认无标题登录_登录另一个帐户 = {"cn": "登录另一个帐户", "en": ""}

    # 通过手机号登录
    UI用手机号登录 = {"cn": "用手机号登录", "en": ""}
    UI用手机号登录_使用其他方式登录 = {"cn": "使用其他方式登录", "en": "login"}
    UI用手机号登录_接受并继续 = {"cn": "接受并继续", "en": ""}
    UI用手机号登录_用微信号QQ号邮箱登录 = {"cn": "用微信号/QQ号/邮箱登录", "en": ""}

    UI通过微信ID邮箱QQID登录= {"cn": "用微信号/QQ号/邮箱登录", "en": ""}
    UI通过微信ID邮箱QQID登录_接受并登录 = {"cn": "同意并登录", "en": "login"}

    同意并登录 = {"cn": "同意并登录", "en": "login"}
    更多选择 = {"cn": "更多选择", "en": ""}

    开始登录验证 = {"cn": "开始登录验证", "en": "Start to verify"}
    选择通过短信验证码 = {"cn": "选择通过短信验证码", "en": "Via SMS Verification Code"}
    确认安全性已完成 = {"cn": "确认安全性已完成", "en": ""}

    左上角左箭头返回 = {"cn": "返回", "en": ""}  # XCUIElementTypeButton
    左上角叉叉关闭 = {"cn": "关闭", "en": ""}
    右上角取消按钮 = {"cn": "取消", "en": ""}

    ### UI主界面 XCUIElementTypeTabBar รายการแถบ
    列表栏 = {"cn": "列表栏", "en": "",}
    主导航_聊天 = {"cn": "聊天", "en": ""}
    主导航_联系人 = {"cn": "联系人", "en": ""}
    主导航_通讯录 = {"cn": "通讯录", "en": ""}
    主导航_发现 = {"cn": "发现", "en": ""}
    主导航_我 = {"cn": "我", "en": ""}
    #
    UI主界面_搜索按钮={"cn": "搜索：", "en": ""}
    UI主界面_聊天搜索_按流派搜索={"cn": "按流派搜索：", "en": ""}
    UI主界面_聊天搜索_正在加载中={"cn": "正在加载…", "en": ""}
    UI主界面_聊天搜索_搜索结果={"cn": "正在加载…", "en": ""}


    def T(self):
        return self.value[define.LANGUAGE]

    def M(self, model):
        if model=="":
            model=define.DEFMOBILEMODEL
        #
        return self.value[model]


    def CN(self):
        return self.value["cn"]
    #
    def EN(self):
        return self.value["en"]

