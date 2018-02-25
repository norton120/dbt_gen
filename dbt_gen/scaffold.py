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
                column_comments = dict((column,comment[3]) for column, comment in self.columns.items() if comment[3] != '' )
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

            comment_block += '\n"{{comment(\'' + column + '\',\'' + comment + '\')}}"'  
            comment_block += ','
        
        comment_block = comment_block[:-1]

        comment_block += '\n]})}}'
 
        return comment_block
        

    def _generate_schema_tests(self):
        schema_test_file_path = self.config['dbt_root_path'] + os.path.sep + 'models' + os.path.sep + self.model_grouping + os.path.sep + 'schema.yml'
        try:
            schema_test_file = open(schema_test_file_path, 'a')
        
        except:
            self.logger.error("Unable to append to schema.yml file: {} : {}".format(sys.exc_info()[0], sys.exc_info()[1]))            
            self._unwind()
            
        not_nulls = []

        uniques = []

        for k, v in self.columns.items():
            if v[1] == 1:
                not_nulls.append(k.lower()) 
            if v[2] == 1:
                uniques.append(k.lower())

        yaml_test_lines = ['']
        yaml_test_lines.append(self.table.upper() + ':')
        yaml_test_lines.append('  constraints:')
        yaml_test_lines.append('    not_null:')

        for n in not_nulls:
            yaml_test_lines.append('      - '+n)
   
        yaml_test_lines.append('')
        yaml_test_lines.append('    unique:')


        for n in uniques:
            yaml_test_lines.append('      - '+n)
        
        schema_test_file.write('\n'.join(yaml_test_lines))
        schema_test_file.write('\n')
    
        schema_test_file.close()

    def generate(self):
        self._generate_file('mid')
        self._generate_file('analytics')
        self._generate_schema_tests()

    def _unwind(self):
        self.logger.error('Unwinding mid and analytics models;')
        try:
            paths_to_models = (self.config['dbt_root_path'] + os.path.sep + 'models' + os.path.sep + self.model_grouping + os.path.sep + 'mid' + os.path.sep + 'MID_' + self.table.upper() + '.sql', 
                               self.config['dbt_root_path'] + os.path.sep + 'models' + os.path.sep + self.model_grouping + os.path.sep + 'analytics' + os.path.sep + self.table.upper() + '.sql')

            for path in paths_to_models:
                os.remove(path)

        except:
            self.logger.error("Unable to unwind scaffolding: {} : {}".format(sys.exc_info()[0], sys.exc_info()[1]))            
        
        sys.exit()


# TODO: add private model layer

    
