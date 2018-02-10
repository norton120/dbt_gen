
import tkinter as tk
import os.path as path
import sys
import yaml
import logging


logger = logging.getLogger('dbt_gen')

def main(args=None):
    
    config_file = path.sep.join([path.expanduser('~'),'.dbt_gen','config.yml'])
    log_file = path.sep.join([path.expanduser('~'),'.dbt_gen','dbt_gen.log'])

    setup_logger(log_file)
   
    config = determine_config_status(config_file)


        

    

 
def determine_config_status(config_file):
    logger.debug('Checking for config file')
    if not path.isfile(config_file):
        # startup config dialog
        logger.info('Config not found. Starting setup dialog.')
        sys.exit()

    logger.info('Config found.')
    return import_config(config_file)



def setup_logger(log_file):
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(log_file)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
    logger.addHandler(handler)
                        

def import_config(config_file):
    try:
        logger.debug('Opening config.')
        config = yaml.load(open(config_file))
    except:
        logger.debug('Failed to open or read config')

    return config

main()
