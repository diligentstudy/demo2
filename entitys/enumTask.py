# 导入枚举类
from enum import Enum

# 自动任务设置
class enumTask(Enum):
    # 配置文件目前支持的自动任务类型
    # 配置文件需要和这里保持一致
    # config.ini fulltask = 获取wxid,通过好友申请,添加好友,获取好友数量,摇一摇,退出微信

    获取wxid = "获取wxid"
    通过好友申请 = "通过好友申请"
    添加好友 = "添加好友"
    获取好友数量 = "获取好友数量"
    摇一摇 = "摇一摇"
    退出微信 = "退出微信"
