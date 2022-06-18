import logging

# LOG_FORMAT   = '%(log_color)s%(levelname)s%(reset)s %(message_log_color)s%(message)s'
#
# #logging.addLevelName(logging.CRITICAL, '[-]')
#
# handler   = colorlog.StreamHandler()
#
# formatter = colorlog.ColoredFormatter(LOG_FORMAT,
#                                       datefmt=DATE_FORMAT,
#                                       reset=True,
#                                       log_colors=LOG_COLORS,
#                                       secondary_log_colors=SECONDARY_LOG_COLORS,
#                                       style='%')
# handler.setFormatter(formatter)
# logger = colorlog.getLogger()
#
# # Add custom levels (not supported by default by logging)
# # https://gist.github.com/hit9/5635505
# logging.SUCCESS = 35
# logging.PROMPT = 36
# logging.SMARTINFO = 37
# logging.SMARTSUCCESS = 38
# logging.SMARTERROR = 39
# logging.addLevelName(logging.DEBUG, DEBUG)
# logging.addLevelName(logging.INFO, INFO)
# logging.addLevelName(logging.WARNING, WARNING)
# logging.addLevelName(logging.ERROR, ERROR)
#
#
#
# logger.setLevel('INFO')
# logger.addHandler(handler)
#
# logging.getLogger('urllib3').setLevel(logging.CRITICAL)
