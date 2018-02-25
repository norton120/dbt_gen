import os
import sys
import time
import yaml
from global_logger import GLOBAL_LOGGER
from dbt_git import dbt_git
from gui import Gui
from warehouse import Warehouse
from scaffold import Scaffold

logger = GLOBAL_LOGGER
win = Gui()
table_selections = dict()

def main(args=None):
         
    global column_preferences 
    column_preferences= dict()

    config_file = os.path.sep.join([os.path.expanduser('~'),'.dbt_gen','config.yml'])
    log_file = os.path.sep.join([os.path.expanduser('~'),'.dbt_gen','dbt_gen.log'])

    config = determine_config_status(config_file)   
    
    model_groups = [folder for folder in os.listdir(config['dbt_root_path'] + os.path.sep + 'models') if os.path.isdir(config['dbt_root_path'] + os.path.sep + 'models' + os.path.sep + folder)]
    
    win.welcome_message()
    win.prepairing_dbt_repo()
    check_out_master(config['dbt_root_path'])
    time.sleep(2)

    win.repo_prepaired()
    time.sleep(3)

    display_lake_tables(gather_lake_tables(config['connector'],config['data_lake_database'],config['data_lake_schemas']),_set_selected_table)

    check_table_eligibility(config['dbt_root_path'])
    

    NEW_BRANCH = (table_selections['approved_schema'] + '-' + table_selections['approved_table']).replace('_','-')

    build_new_repo(config['dbt_root_path'], NEW_BRANCH)

    columns = gather_potential_columns(config['connector'],config['data_lake_database'])
    
    display_potential_columns(columns, _set_column_preferences)    
    
    select_model_group(model_groups, _set_model_group)
    
    generate_scaffold(config,column_preferences,table_selections['model_grouping'],table_selections['approved_schema'],table_selections['approved_table'])

    commit_changes(config['dbt_root_path'], NEW_BRANCH)
    time.sleep(2)

    push_to_origin(config['dbt_root_path'], NEW_BRANCH)
    time.sleep(2)

    win.completed()
    
def check_out_master(repo):
    dgit = dbt_git(repo)
    try:
        dgit.prep_repo()
    except:
        win.failed_to_prepare_repo()
        time.sleep(3)
        sys.exit()

def gather_lake_tables(creds, database, schema):
    win.gathering_lake_tables()
    wh = Warehouse(creds)
    return wh.get_lake_tables(database,schema)

def display_lake_tables(tables, callback):
    return win.select_lake_table(tables,callback)

def _set_selected_table(table):
    table_selections['requested_table'] = table       

def check_table_eligibility(root_path):
    
    win.checking_selection()
    table = table_selections['requested_table'].split('.')
    for directory,folder, files in os.walk(root_path + os.path.sep + 'models'):
        for file_name in files:
            if file_name.upper() in (table[1].upper().strip() + '.SQL','MID_' + table[1].upper().strip() + '.SQL'):
                win.reject_selection(file_name)        

    table_selections['approved_schema'] = table[0].lower()        
    table_selections['approved_table'] = table[1].lower()        
        
def build_new_repo(repo, new_branch):
    dgit = dbt_git(repo)

    if not dgit.create_new_branch(new_branch):
        win.failed_to_build_repo(new_branch)

def gather_potential_columns(creds,database):
    wh = Warehouse(creds)
    return wh.get_table_columns(database,table_selections['approved_schema'],table_selections['approved_table'])

def display_potential_columns(columns,callback):
    return win.column_matrix(columns,callback)
    
def _set_column_preferences(updated_preferences):
    global column_preferences
    column_preferences = updated_preferences

def select_model_group(model_groups,callback):
    win.select_model_group(model_groups, callback)
            
def _set_model_group(selected_model_group):
    global table_selections
    table_selections['model_grouping'] = selected_model_group

def generate_scaffold(config,column_preferences,model_grouping,schema,table):
    win.generating_models_and_tests()  
    scaffold = Scaffold(config,column_preferences,model_grouping,schema,table)
    scaffold.generate()

def commit_changes(repo,new_branch):
    win.committing_and_pushing()
    dgit = dbt_git(repo)
    if not dgit.commit(new_branch):
        win.commit_failed()       
        time.sleep(2)
        sys.exit()

def push_to_origin(repo, new_branch):
    dgit = dbt_git(repo)
    if not dgit.push_to_origin(new_branch):
        win.push_failed()
        time_sleep(2)
        sys.exit()


def determine_config_status(config_file):
    logger.debug('Checking for config file')
    if not os.path.isfile(config_file):
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
