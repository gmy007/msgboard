import logging

logger_name = 'mainLogger'

logger = logging.getLogger(logger_name)
logger.setLevel(level=logging.INFO)

fileHandler = logging.FileHandler('log.txt')
fileHandler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(name)s  %(levelname)-8s: %(message)s')
fileHandler.setFormatter(formatter)

console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(formatter)

logger.addHandler(fileHandler)
logger.addHandler(console)