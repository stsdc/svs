# Create a logger object.
import logging
import coloredlogs
import os

os.environ['COLOREDLOGS_LOG_FORMAT'] ='%(asctime)s.%(msecs)03d %(name)s - %(message)s'
os.environ['COLOREDLOGS_DATE_FORMAT'] ='%H%M%S'
# os.environ['COLOREDLOGS_LEVEL_STYLES'] ='info=cyan,bold;warning=yellow;error=red;critical=red,bold'
logger = logging.getLogger("SVSystem")

coloredlogs.install(level='DEBUG')

# class Logger:
#     def __init__(self, module_name, level):
#         os.environ['COLOREDLOGS_LOG_FORMAT'] ='%(asctime)s.%(msecs)03d %(name)s - %(message)s'
#         os.environ['COLOREDLOGS_DATE_FORMAT'] ='%H%M%S'
#         self.logger = logging.getLogger(module_name)
#         coloredlogs.install(level=level)
#
#     def debug(self, msg):
#         self.logger.debug(msg)
#
#     def info(self, msg):
#         self.logger.info(msg)
#
#     def warn(self, msg):
#         self.logger.warn(msg)
#
#     def error(self, msg):
#         self.logger.error(msg)
#
#     def critical(self, msg):
#         self.logger.critical(msg)
