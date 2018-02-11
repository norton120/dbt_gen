from global_logger import GLOBAL_LOGGER


class Warehouse:
    
    platform = ''

    def __init__(self,platform):
    # platform is the warehouse type from config. 
        self.platform = platform    
    
    def get_lake_tables(self, database, schemas):
        pass

    def get_table_columns(self, database, schema, table):
        pass

