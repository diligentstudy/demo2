# wda包名
WEBAGENT="com.facebook.WebDriverAgentRunner.xctrunner"
# 短信服务器地址
MOBILEMSG_IP = "192.168.2.240"
# 主服务器-保存账号信息接口
HOSTSERVER="http://192.168.2.240:58800"
# 接口授权令牌
AUTHORIZATION="ox7Sd_*6DZN*eUKCf9^3Pt$!CN2+=7P_bBDMktzwXu8Z09gEJ%gFHwGVp40bM*sj"

FULLTASKMODE="wx登录,wx注册"
CURTASKMODE="wx登录"
DEFMOBILEMODEL="iPhone 7"
# 启动目录
STARTPATH=""
# sys.executable 当前的Python解释器路径
EXECUTABLE="/usr/bin/python"
# backupAPP路径
BACKUPAPP="/Volumes/Work/softbag/ipa/xxx1.ipa"
# 目标APP路径
THEIPAFILE="/Volumes/Work/softbag/ipa/xxx2.ipa"
# 是否必须重装APP
NEEDREINSTALL=False
# 允许自动拖图
ALLOWAUTODRAG=False
# 刷新新图后等待秒数
DRAGIMGWAITLOAD=4
# 拖图微调校准
DRAGALIGIN=0
# 拖图识别忽略的左边区域宽度
DRAGSKIPWIDTH=190

# 一直保持循环keepactive
KEEPACTIVE=True
# 每次登录必须开关飞行模式
FIGHTMODESWG=True
#备份时是否备份好友数据
BACKFRIEND=False
# 账号退出时是重装APP reinstall 还是刷底包 reflash
LOGOUTACCESS="reflash"
#
# 发送好友请求后等待多少秒 waitafterfriendreq
WAITAFTERFRIENDREQ=120
# SETTING
# 多语言支持 cn,en
LANGUAGE="cn"
# 目标APP 包名
PACKAGENAME="com.tencet.xin"
# 目标端口
WDAPORT = 8100
#WEBAPI循环调用等待秒数
APISLEEP=3
# 获取短信循环等待秒数
APISMSSLEEP = 5
# 获取短信超时秒数
APISMSWAIT = 60
# 允许重新登录
ALLOWRELOGIN=True

# 忽略登录的账号，测试使用
SKIPUSERS=""
#指定测试账号 ----
TESTUSER=""
#必须重新登录，
# True: 如果已经在线也有先下线再登录，
# False: 如果已经在线就不用重新登录
MUSTRELOGIN=False
MUSTREIMGBAK=False

# 区号配置
AREACODE="+86"
# 数据备份路径
IMGSTORE="/Volumes/Work/imgstore"
# 随机打招呼消息
TALKS=["hi","hello","How are you","how do you do","Hi, nice to meet you"]

# 自动任务设置
# 目前支持的自动任务类型：
TASK_FULL = []
# 当前配置的任务
TASK_CURSET = []
# 任务运行开关，False 不开启，True 开启
TASK_RUNSWG = False

#######
# 数据库配置
# MYSQL
# DBHOST = ""
# DBPORT = 0
# DBUSER = ""
# DBPWD = ""
# DBNAME = ""
# DBCHAR = "utf8"

SJK_LOGIN="s1"
SJK_LOGIN_REPORT="s2"
SJK_REG="s3"
SJK_REG_REPORT="s4"
SJK_REG_UP_QRCODE="s5"
SJK_REPORT_NEEDFRIEND="s6"