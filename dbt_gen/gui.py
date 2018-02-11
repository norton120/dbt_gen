from tkinter import *

class Gui:
    
    window = Tk()
    
    def __init__(self):
        self.window.title('DBT Gen: model template engine')
        self.window.mainloop()

    def welcome_message(self):
        pass
    def prepairing_dbt_repo(self):
        pass
    def failed_to_prepare_repo(self):
        pass
    def gathering_lake_tables(self):
        pass
    def select_lake_table(self, tables):
        pass
    def reject_selection(self, reason):
        pass
    def column_matrix(self, columns):
    # all the columns in rows, with checkboxes for: exclude, not null, unique
    # and input for comment
        pass
    def generating_models_and_tests(self, table_name):
        pass
    def committing_and_pushing(self):
        pass
    def commit_failed(self):
        pass
    def completed(self):
        pass


