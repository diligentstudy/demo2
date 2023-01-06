
# 连接的手机信息类
class IPhoneInfo:
    def __init__(self):
        self.UDID = ""              # uuid
        self.SerialNumber = ""      # 序列号
        self.NAME = ""              # 名称
        self.MarketName = ""        # 上市名称
        self.ProductVersion = ""    # 产品版本
        self.ConnType = ""          # 连接类型
        self.Status = ""            # 运行消息提示
        self.State = 0              # 运行状态 0 停止 1 正在运行
        self.RowIndex = 0           # 行的索引 唯一
        self.RowNo = 0              # 行的ID 唯一
        # self.list = []            # 列表
