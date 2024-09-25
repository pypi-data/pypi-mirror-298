import logging
import os
from logging.handlers import RotatingFileHandler

from octopus_common.constant import constants


def init_log_config():
    # 配置日志目录
    log_dir = constants.LOGGING_DIRECTOR
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # 创建 RotatingFileHandler 处理程序
    file_handler = RotatingFileHandler(
        os.path.join(log_dir, 'application.log'),
        maxBytes=50 * 1024 * 1024,
        backupCount=10
    )
    file_handler.setLevel(logging.INFO)

    # 创建 StreamHandler 处理程序
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # 设置日志格式
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # 配置全局 logging
    logger = logging.getLogger()
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.setLevel(logging.INFO)
