from tkinter import *

class Gui:
    
    window = Tk()
    
    def __init__(self):
        self.window.title('DBT Gen: model template engine')

    def welcome_message(self):
        pass
    def prepairing_dbt_repo(self):
        pass
    def failed_to_prepare_repo(self):
        pass
    def gathering_lake_tables(self):
        pass
    def select_lake_table(self, tables):

            
        scrollbar = Scrollbar(self.window)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        listbox = Listbox(self.window, yscrollcommand=scrollbar.set)
        for i in tables:
            listbox.insert(END, i[0]+'.'+i[1])
        listbox.config(width=80, height=80)
        listbox.pack(side=LEFT, fill=X, padx=3)
        
        scrollbar.config(command=listbox.yview)
        self.window.mainloop()
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


