from global_logger import GLOBAL_LOGGER
import sys

class Warehouse:
    
    logger = GLOBAL_LOGGER
    
    platform = ''

    def __init__(self,creds):
    # platform is the warehouse type from config. 
        self.creds = creds
        if self.creds['type'] == 'snowflake':
            import snowflake.connector as db            
            try:
                self.con = db.connect(user= self.creds['user'],
                    password= self.creds['password'],
                    account= self.creds['account']
                    )
            except:
                self.logger.error('Failed to connect to snowflake: {}'.format(sys.exc_info()[0]))
                return False


    def get_lake_tables(self, database, schemas):
        if self.creds['type'] == 'snowflake':
            cursor = self.con.cursor()
            tables = [] 
            try:

                for schema in schemas:
                    cursor.execute("SELECT table_name from {}.information_schema.tables WHERE table_schema = '{}'".format(database,schema.upper()))
                    for name in cursor:
                        tables.append((schema.upper(),name[0]))
            except:
                self.logger.error('Failed to gather tables from data lake: {}'.format(sys.exc_info()[0]))
                return False               
            
            return tables

    def get_table_columns(self, database, schema, table):
        if self.creds['type'] == 'snowflake':
            cursor = self.con.cursor()
            columns = []
            try:
                cursor.execute("SELECT column_name FROM {}.information_schema.columns WHERE table_schema = '{}' AND table_name = '{}'".format(database,schema.upper(),table.upper()))
                for column in cursor:
                    columns.append(column[0])
            except:
                self.logger.error('Failed to gather columns from data lake: {}'.format(sys.exc_info()[0]))
                return False

            return columns
