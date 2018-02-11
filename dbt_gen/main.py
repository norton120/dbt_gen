import os.path as path
import sys
import time
import yaml
from global_logger import GLOBAL_LOGGER
from dbt_git import dbt_git
from gui import Gui
from warehouse import Warehouse

logger = GLOBAL_LOGGER
win = Gui()
 
def main(args=None):
          
    config_file = path.sep.join([path.expanduser('~'),'.dbt_gen','config.yml'])
    log_file = path.sep.join([path.expanduser('~'),'.dbt_gen','dbt_gen.log'])
   
    config = determine_config_status(config_file)   

    check_out_master(config['dbt_root_path'])
    
    display_lake_tables(gather_lake_tables(config['connector'],config['data_lake_database'],config['data_lake_schemas']))
    exit();
    
def check_out_master(repo):
    dgit = dbt_git(repo)
    if dgit.prep_repo():
        pass
        win.gathering_lake_tables()
    else:
        win.failed_to_prepare_repo()
        time.sleep(5)
        sys.exit()

def gather_lake_tables(creds, database, schemas):
    wh = Warehouse(creds)
    return wh.get_lake_tables(database,schemas)

def display_lake_tables(tables):
    win.select_lake_table(tables)
 
def determine_config_status(config_file):
    logger.debug('Checking for config file')
    if not path.isfile(config_file):
        # startup config dialog
        logger.debug('Config not found. Starting setup dialog.')
        sys.exit()

    logger.info('Config found.')
    return import_config(config_file)
                        

def import_config(config_file):
    try:
        config = yaml.load(open(config_file))
    except:
        logger.debug('Failed to open or read config')

    return config

main()
