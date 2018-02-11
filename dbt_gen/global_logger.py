import logging


global_logger = logging.getLogger('dbt_gen')
global_logger.setLevel(logging.DEBUG)
#TODO: need to figure out where this log file should go
handler = logging.FileHandler("dbt_gen.log")
handler.setLevel(logging.DEBUG)
handler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
global_logger.addHandler(handler)

GLOBAL_LOGGER = global_logger
