import os
import subprocess

from entitys import define

def tidExec(cmd):
    proc = subprocess.Popen(
        cmd,        #"{} & {}".format(define.EXECUTABLE ,cmd), 怎么保证是在define.EXECUTABLE的环境执行
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        stdin=subprocess.PIPE  # 重定向输入值
    )
    proc.stdin.close()  # 既然没有命令行窗口，那就关闭输入
    result = proc.stdout.read()  # 读取cmd执行的输出结果（是byte类型，需要decode）
    proc.stdout.close()
    return result.decode(encoding="utf-8")

def exec(cmd):
    proc = subprocess.Popen(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        stdin=subprocess.PIPE  # 重定向输入值
    )
    proc.stdin.close()  # 既然没有命令行窗口，那就关闭输入
    result = proc.stdout.read()  # 读取cmd执行的输出结果（是byte类型，需要decode）
    proc.stdout.close()
    return result.decode(encoding="utf-8")

def exec2(cmd):
    subprocess.Popen(
        cmd,
        shell=True,
        stdout=None,
        stderr=None,
        stdin=None  # 重定向输入值
    )
    # proc.stdin.close()  # 既然没有命令行窗口，那就关闭输入
    # os.spawnl(os.P_NOWAIT, cmd)
