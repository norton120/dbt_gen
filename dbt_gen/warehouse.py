from global_logger import GLOBAL_LOGGER


class Warehouse:
    
    platform = ''

    def __init__(self,creds):
    # platform is the warehouse type from config. 
        self.creds = creds
            
    
    def get_lake_tables(self, database, schemas):
        if self.creds['type'] == 'snowflake':
            import snowflake.connector
            try:
                con = snowflake.connector.connect(user= self.creds['user'],
                    password= self.creds['password'],
                    account= self.creds['account']
                    )
                cursor = con.cursor()
            except:
                self.logger.error('Failed to connect to snowflake')
                return False
            
            tables = [] 
            try:

                for schema in schemas:
                    cursor.execute("SELECT table_name from {}.information_schema.tables WHERE table_schema = '{}'".format(database,schema.upper()))
                    for name in cursor:
                        tables.append((schema.upper(),name[0]))
            except:
                self.logger.error('Failed to query tables from data lake.')
                return False               
            
            return tables

    def get_table_columns(self, database, schema, table):
        pass

