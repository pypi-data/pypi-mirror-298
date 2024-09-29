import logging


def init_logger(log_dir, log_level):
    logger = logging.getLogger()
    if log_level == 'DEBUG':
        logger.setLevel(logging.DEBUG)
    elif log_level == 'INFO':
        logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(filename="./grazie.log")
    if log_level == 'DEBUG':
        file_handler.setLevel(logging.DEBUG)
    elif log_level == 'INFO':
        file_handler.setLevel(logging.INFO)
    fmt = logging.Formatter(
        fmt="%(asctime)s - %(levelname)s - %(message)s",
    )
    file_handler.setFormatter(fmt)
    logger.addHandler(file_handler)
    return logger


logger = init_logger("#", "DEBUG")
logger.info(
    "啟動：\n"
)
