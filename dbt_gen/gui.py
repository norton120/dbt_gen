from tkinter import *

class Gui:
    
    window = Tk()
    v = StringVar()


    def __init__(self):
        self.window.minsize(800,500)
        self.window.title('DBT Gen: model template engine')
        self.v.set('Prepairing your local repo..')

    def welcome_message(self):
        welcome = Label(self.window, text="DBT Gen", font=('Impact',20))
        welcome.grid(row=0, column=0, columnspan=20)
        self.window.update()

    def prepairing_dbt_repo(self):
        text = Label(self.window, textvariable=self.v, font=('Impact',16))
        text.grid(row=1, column=0, columnspan=20)
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
        frame = Frame(self.window, bd=2, relief=SUNKEN)

        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        _locals = {"selecting_table":True}

        self.v.set("Please select the data lake table to be transformed:")
            
        self.scrollbar = Scrollbar(self.window)
        self.scrollbar.grid(row=0, column=1, sticky=N+S)
        
        self.listbox = Listbox(self.window, yscrollcommand=self.scrollbar.set)
        for i in tables:
            self.listbox.insert(END, i[0]+'.'+i[1])
        self.listbox.config(width=90, height=45)
        self.listbox.grid(row=4, column=0, columnspan=10, rowspan=10, padx=1)
        self.scrollbar.config(command=self.listbox.yview)
        
        def select_table_click():
            callback(self.listbox.get(self.listbox.curselection()))    
            _locals['selecting_table'] = False

        self.button = Button(self.window, text= "select table", command = select_table_click)
        self.button.grid(row=12, column= 8)
        
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

    def column_matrix(self, columns, callback):
        _locals = {'setting_up_columns':True}

        self.matrix = Frame(self.window, background="black")

        self.checkbox_vars = dict()
   
        for column in columns:
            self.checkbox_vars[column] = [IntVar(), IntVar(),IntVar(),StringVar()]

        self.matrix._widgets = []
        
        header = []
        header.append(Label(self.window, text = "Column Name", borderwidth=0, width= 15))
        header.append(Label(self.window, text = "Not Null?", borderwidth=0, width= 10))
        header.append(Label(self.window, text = "Unique?", borderwidth=0, width= 10))
        header.append(Label(self.window, text = "Description", borderwidth=0, width= 10))
        
        for index, col in enumerate(header):
            col.grid(row=0, column=index, sticky="nsew", padx=1,pady=1)        

        self.matrix._widgets.append(header)
        for row in range(len(columns)-1):
            current_row = []
            current_row.append(Label(self.window, text = columns[row], borderwidth=0, width= 15))
            current_row.append(Checkbutton(self.window, variable=self.checkbox_vars[columns[row]][0]))
            current_row.append(Checkbutton(self.window, variable=self.checkbox_vars[columns[row]][1]))
            current_row.append(Entry(self.window, text='', textvariable=self.checkbox_vars[columns[row]][2]))

            for index, r in enumerate(current_row):
                r.grid(row=row,  column=index, sticky="nsew", padx=1,pady=1)

            self.matrix._widgets.append(current_row)
        
        for col in range(5):
            self.matrix.grid_columnconfigure(col, weight=1)

        self.matrix.grid()
        
        def submit_columns():
            finalized_input_values = dict()
            for col, values in self.checkbox_vars.items():
                finalized_input_values[col] = []
                for val in values:
                    finalized_input_values[col].append(val.get())
            callback(finalized_input_values)
            _locals['setting_up_columns'] = False        

        self.button = Button(self.window, text= "Create Models", command = submit_columns)
        self.button.grid(row=12, column= 8)

        while _locals['setting_up_columns']:
            self.window.update()
        
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



