import os
from global_logger import GLOBAL_LOGGER




class Scaffold:
    
    logger = GLOBAL_LOGGER

    def __init__(config,column_preferences,model_grouping,schema,table):
        self.config = config
        self.colums = column_preferences
        self.model_grouping = model_grouping
        self.schema = schema
        self.table = table


    def _generate_mid(self):
        self.logger.debug("Generating mid model...")            
        try:
            target = open(config['dbt_root_path'] + os.path.sep + 
                          'models' + os.path.sep + self.model_grouping + 
                          os.path.sep + 'MID_' + os.path.sep + self.columns.table.upper() + '.sql', 'w')
        except:
            self.logger.error("Unable to write to mid model: {}".format(sys.exec_info[0]))            
            return False
        
        try:
            template = open(self.config['dbt_root_path'] + os.path.sep + 
                            'templates' + os.path.sep + 'mid_' + self.config['templates'].get(self.model_grouping, self.config['default']) + '.sql' ,'r')  

            exceptions = [("'" + c + "'" ) for c,options in column_preferences if options[0] == 1]   
            
            line = template.readline()
            while line.endswith('\n'):
                line = line.replace('%%DATABASE%%', "'{}'".format(self.config['data_lake_database'].upper())
                line = line.replace('%%SCHEMA%%', "'{}'".format(self.schema.upper()) 
                line = line.replace('%%TABLE%%', "'{}'".format(self.table.upper()) 
                line = line.replace('%%EXCEPT%%', "'[{}]'".format(','.join(exceptions).upper()) 
                 
                
                

        except: 
            pass
        

    def _generate_public(self):
        pass

    def _generate_schema_tests(self):
        pass

# TODO: add private model layer

    
