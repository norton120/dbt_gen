from tkinter import *

class Gui:
    
    window = Tk()
    v = StringVar()


    def __init__(self):
        self.window.title('DBT Gen: model template engine')
        self.v.set('Prepairing your local repo..')

    def welcome_message(self):
        welcome = Label(self.window, text="DBT Gen", font=('Impact',20))
        welcome.pack(expand=YES, fill=BOTH)
        self.window.update()

    def prepairing_dbt_repo(self):
        text = Label(self.window, textvariable=self.v, font=('Impact',16))
        text.pack(expand=YES, fill=BOTH)
        self.window.update()

    def repo_prepaired(self):
        self.v.set("updated")
        self.window.update()

    def failed_to_prepare_repo(self):
        self.v.set("ERROR: unable to update your local repo")
        self.window.update()

    def gathering_lake_tables(self):
        self.v.set("Gathering tables from Data Lake...")
        self.window.update()

    def select_lake_table(self, tables):
        self.v.set("Please select the data lake table to be transformed:")
            
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



