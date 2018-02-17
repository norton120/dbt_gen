import os
import sys
from global_logger import GLOBAL_LOGGER




class Scaffold:
    
    logger = GLOBAL_LOGGER

    def __init__(self,config,column_preferences,model_grouping,schema,table):
        self.config = config
        self.columns = column_preferences
        self.model_grouping = model_grouping
        self.schema = schema
        self.table = table


    def _generate_mid(self):
        self.logger.debug("Generating mid model...")            
        try:
            target = open(self.config['dbt_root_path'] + os.path.sep + 
                          'models' + os.path.sep + self.model_grouping + 
                          os.path.sep + 'mid' + os.path.sep + 'MID_' + self.table.upper() + '.sql', 'w')
        except:
            self.logger.error("Unable to write to mid model: {} : {}".format(sys.exc_info()[0], sys.exc_info()[1]))            
            return False
        
        try:
            self.logger.debug("Gathering template..")
            
            mid_template_source = self.config['templates'].get(self.model_grouping, self.config['templates']['default']) + os.path.sep +  'mid_template.sql'
            
            template = open(self.config['dbt_root_path'] + os.path.sep + 'templates' + os.path.sep + mid_template_source,'r')  
        except:
            self.logger.error("Unable to read mid model template: {} : {}".format(sys.exc_info()[0], sys.exc_info()[1]))            
            return False    
            
        self.logger.debug("Gathered template {} ".format(mid_template_source))
        
        try:
            exceptions = [("'{}'".format(c)) for c,options in self.columns.items() if options[0] == 1]   

            line = template.readline()

            while line.endswith('\n'):
                line = line.replace('%%DBT_GEN_DATABASE%%', "{}".format(self.config['data_lake_database'].upper()))
                line = line.replace('%%DBT_GEN_SCHEMA%%', "{}".format(self.schema.upper()))
                line = line.replace('%%DBT_GEN_TABLE%%', "{}".format(self.table.upper()))                 
                line = line.replace('%%DBT_GEN_EXCEPTIONS%%', "{}".format(','.join(exceptions)))
                target.write(line)
                line = template.readline()

        except:
            self.logger.error("Unable to load variables into template: {} : {}".format(sys.exc_info()[0], sys.exc_info()[1]))            
            self._unwind()
        
        target.close()


    def _generate_public(self):
        pass

    def _generate_schema_tests(self):
        pass

    def generate(self):
        self._generate_mid()
        self._generate_public()
        self._generate_schema_tests()

    def _unwind(self):
        pass

# TODO: add private model layer

    
