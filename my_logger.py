import logging

def init_mylogger(logger_name,logfile_path, loglevel=logging.DEBUG):
    logger = logging.getLogger(logger_name)

    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')

    fileHandler = logging.FileHandler(logfile_path)
    fileHandler.setFormatter(formatter)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)

    logger.addHandler(fileHandler)
    logger.addHandler(streamHandler)

    fileHandler.setLevel(logging.DEBUG)
    streamHandler.setLevel(logging.INFO)

    logger.setLevel(logging.DEBUG)

