# 导入枚举类
from enum import Enum, unique

# 重置类型
class ResetType(Enum):
    Normal = 0          # 正常
    ResetScript = 1     # 重置脚本
    ResetScriptUser = 2 # 重置脚本和用户

# 任务类型
class TaskMode(Enum):
    wx自动注册 = 0  # wx自动注册
    wx自动登录 = 1  # wx自动登录
