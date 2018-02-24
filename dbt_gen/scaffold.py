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



    def _generate_file(self,layer):
        self.logger.debug("Generating mid model...")          
        prefix = 'MID_' if layer.upper() == 'MID' else ''
  
        try:
            target = open(self.config['dbt_root_path'] + os.path.sep + 
                          'models' + os.path.sep + self.model_grouping + 
                          os.path.sep + layer.lower() + os.path.sep + prefix + self.table.upper() + '.sql', 'w')
        except:
            self.logger.error("Unable to write to {} model: {} : {}".format(layer,sys.exc_info()[0], sys.exc_info()[1]))            
            return False
        
        try:
            self.logger.debug("Gathering template..")
            
            template_source = self.config['templates'].get(self.model_grouping, self.config['templates']['default']) + os.path.sep + layer.lower() + '_template.sql'
            
            template = open(self.config['dbt_root_path'] + os.path.sep + 'templates' + os.path.sep + template_source,'r')  
        except:
            self.logger.error("Unable to read {} model template: {} : {}".format(layer,sys.exc_info()[0], sys.exc_info()[1]))            
            return False    
            
        self.logger.debug("Gathered template {} ".format(template_source))
        
        try:
            exceptions = [("'{}'".format(c)) for c,options in self.columns.items() if options[0] == 1]   

            line = template.readline()

            while line.endswith('\n'):
                line = line.replace('%%DBT_GEN_DATABASE%%', "{}".format(self.config['data_lake_database'].upper()))
                line = line.replace('%%DBT_GEN_SCHEMA%%', "{}".format(self.schema.upper()))
                line = line.replace('%%DBT_GEN_TABLE%%', "{}".format(self.table.upper()))                 
                line = line.replace('%%DBT_GEN_EXCEPTIONS%%', "{}".format(','.join(exceptions)))
                line = line.replace('%%DBT_GEN_MID_MODEL%%', "{}".format('MID_'+self.table.upper()))
                target.write(line)
                line = template.readline()

            if layer == 'analytics':
                column_comments = {(column,comment[3]) for column, comment in self.columns.items() if comment[3] != '' }
                target.write(self._add_comments(column_comments)) 

        except:
            self.logger.error("Unable to load variables into template: {} : {}".format(sys.exc_info()[0], sys.exc_info()[1]))            
            self._unwind()
        
        self.logger.debug("created {} model at {}".format(layer,target.name))
        target.close()

    def _add_comments(self,column_comments):
        comment_block = ''' 
                        {{ config({
                            "post-hook":[
                        '''

        for column, comment in column_comments.items():
            # scrub quotes, since people always add them 
            comment = comment.replace("'","`").replace('"','`') 

            comment_block += '"{{comment(\'' + column + '\',\'' + comment + '\')}}"'  
            if not loop.last():
                comment_block += ','
            comment_block += '\n'

        comment_block += ']})}}'
 
        return comment_block
        

    def _generate_schema_tests(self):
        pass

    def generate(self):
        self._generate_file('mid')
        self._generate_file('analytics')
        self._generate_schema_tests()

    def _unwind(self):
        pass

# TODO: add private model layer

    
