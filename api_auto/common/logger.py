# import logging
# #日志收集器---笔  -TY是日志收集器的名称
# logger = logging.getLogger("TY")
# #这支笔只记录"INFO"以上的等级信息  --设置级别
# logger.setLevel('INFO')
#
# #初始化Handler处理器   ---在控制台显示 --日记本1
# handler = logging.StreamHandler()
# #日记本1收录"INFO"以上的等级信息
# handler.setLevel('INFO')
#
# #初始化文件Handler处理器   ---在TY.log文件显示  --日记本2
# file_handler = logging.FileHandler('TY.log',encoding='utf-8')
# #日记本2收录"INFO"以上的等级信息
# file_handler.setLevel('INFO')
#
# #处理器和收集器绑定在一起，纸和笔绑定在一起
# logger.addHandler(handler)
# logger.addHandler(file_handler)
#
# # #获取格式1
# # console_fmt = logging.Formatter(style="{",
# # fmt="{asctime}: {name}: {levelname}: {filename} : {lineno}: {message}",
# # datefmt="%Y/%m/%d %H:%M:%S")
# # #将处理器和格式绑定在一起
# # handler.setFormatter(console_fmt)
#
# #设置格式2
# console_fmt =logging.Formatter(
# fmt="%(name)s-%(levelno)s-%(filename)s-%(lineno)d-%(asctime)s-%(message)s")
# #将处理器和格式绑定在一起
# handler.setFormatter(console_fmt)        #控制器应用格式
# file_handler.setFormatter(console_fmt)   #文件应用格式
#
# #正式去记录需要获取的日志
# logger.debug("调试信息")
# logger.info("正在读取测试数据")
# logger.warning("警告信息")
# logger.error("错误信息")


# from loguru import logger
# logger.add(sink="TY.log", encoding='utf-8',
# rotation='1KB',compression='zip')
# logger.info("这是info")
# logger.warning ("这是warning")
# logger.error("这是错误")

from loguru import logger
from api_auto.config.config import Config
def get_log(sink="TY.log", rotation='10MB'):
    logger.add(sink=sink,encoding='utf-8',rotation=rotation)
    return logger

# log 变量会用到所有其他的模块中，想用的时候直接导入 log 变量
log = get_log(Config.LOG_FILE)
print(log)


# if __name__ == '__main__' :
#     log = get_log()
#     log.info ("helLo")






