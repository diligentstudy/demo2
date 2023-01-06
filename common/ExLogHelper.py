import functools
import logging

from entitys import define


def create_logger():
    logger = logging.getLogger("ex_log")
    logger.setLevel(logging.INFO)
    if define.STARTPATH !="":
        lpath="{}/logs/ex_log.log".format(define.STARTPATH)
    else:
        lpath="./logs/ex_log.log"

    fh = logging.FileHandler(lpath)

    fmt = "[%(asctime)s-%(name)s-%(levelname)s]: %(message)s"
    formatter = logging.Formatter(fmt)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger


# # 不返回值，和返回1个值的函数使用正常
# # 如果是返回两个值的函数使用就会异常 异常：cannot unpack non-iterable NoneType object
def log_exception(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs): # *args, **kwargs
        logger = create_logger()
        try:
            fn(*args, **kwargs)  # # *args, **kwargs
        except Exception as e:
            logger.exception("[Error in {}] msg: {}".format(__name__, str(e)))
            raise
    return wrapper

# @log_exception
# def xtain(x):
#     a = input("输入一个数：")
#     if not a.isdigit():
#         raise ValueError("a 必须是数字")
#

#
# if __name__ == '__main__':
#     xtain1(1)