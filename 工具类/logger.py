import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

def setup_logger(name: str, log_file: str = "hydro_monitoring.log"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # 文件日志（自动轮转）
    file_handler = RotatingFileHandler(
        Path("logs") / log_file,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)

    # 控制台日志
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console_handler.setFormatter(console_formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger