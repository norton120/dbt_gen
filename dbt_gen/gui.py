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
        self.v.set("MASTER repo checked out and current with production")
        self.window.update()

    def failed_to_prepare_repo(self):
        self.v.set("ERROR: unable to update your local repo")
        self.window.update()

    def gathering_lake_tables(self):
        self.v.set("Gathering tables from Data Lake...")
        self.window.update()

    def select_lake_table(self, tables,callback):
        _locals = {"selecting_table":True}

        self.v.set("Please select the data lake table to be transformed:")
            
        self.scrollbar = Scrollbar(self.window)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        
        self.listbox = Listbox(self.window, yscrollcommand=self.scrollbar.set)
        for i in tables:
            self.listbox.insert(END, i[0]+'.'+i[1])
        self.listbox.config(width=80, height=80)
        self.listbox.pack(side=LEFT, fill=X, padx=3)
        self.scrollbar.config(command=self.listbox.yview)
        
        def select_table_click():
            callback(self.listbox.get(self.listbox.curselection()))    
            _locals['selecting_table'] = False

        self.button = Button(self.window, text= "select table", command = select_table_click)
        self.button.pack()
        
        while _locals['selecting_table']:
            self.window.update()
        
    def checking_selection(self):
        self.listbox.destroy()
        self.scrollbar.destroy()
        self.button.destroy()
        self.v.set("Checking your selection and building your repo..")    
        self.window.update()

    def reject_selection(self, existing_model):
        self.v.set("Warning: the model {} already exits. Unable to build repo.".format(existing_model))    
        self.window.mainloop()

    def getting_table_columns(self,table):
        pass

    def column_matrix(self, columns):
    # all the columns in rows, with checkboxes for: exclude, not null, unique
    # and input for comment
        pass

    def select_model_group(self, model_groups):
        pass

    def generating_models_and_tests(self, table_name):
        pass
    def committing_and_pushing(self):
        pass
    def commit_failed(self):
        pass
    def completed(self):
        pass



