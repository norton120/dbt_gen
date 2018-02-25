from tkinter import *

class Gui:
    
    window = Tk()
    v = StringVar()


    def __init__(self):
        self.window.geometry('660x650')
        self.window.title('DBT Gen: model template engine')
        
        # build containers
        self.header = Frame(self.window, width=650, height=50, pady=3)
        self.body = Frame(self.window,  width=650, height=500, pady=3)
        self.footer = Frame(self.window, width= 650, height= 100, pady=3)    
        self.footer_button_box = Frame(self.footer, width= 350, height= 100, pady=3)

        # configure the parent window grid
        self.window.grid_rowconfigure(1, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        
        # arrange containers
        self.header.grid(row=0, sticky= 'ew')
        self.body.grid(row=1,sticky='nsew')
        self.body.grid_columnconfigure(0,weight=1)
        self.body.grid_rowconfigure(0,weight=1)
        self.footer.grid(row=3, sticky='ew')    
        self.footer.grid_columnconfigure(1,weight=1)
        self.footer_button_box.grid(row=1, column=2, sticky='w')
        
        self.header.grid_rowconfigure(1,weight=1)
        self.header.grid_columnconfigure(0,weight=1)

        self.headline = Label(self.header, text="DBT Gen", font=('Impact',20))

        self.headline.grid(row=0)
        
        
        self.marquee = StringVar()
        self.marquee_label = Label(self.header, textvariable=self.marquee, font=('Impact',16))
        self.marquee_label.grid(row=1)

    def __str__(self):
        print("Tkinter GUI")

    def _set_marquee(self,headline):
        self.marquee.set(headline)

    def _clear_children(self,obj):
        for child in obj.winfo_children():
            child.destroy()

    def welcome_message(self):
        self._set_marquee('Data Build Tool Template Generator')
        self.window.update()

    def prepairing_dbt_repo(self):
        self._set_marquee('Prepairing your repo...')
        self.window.update()

    def repo_prepaired(self):
        self._set_marquee('MASTER repo checked out and current with production')
        self.window.update()

    def failed_to_prepare_repo(self):
        self._set_marquee("ERROR: unable to update your local repo")
        self.window.update()

    def gathering_lake_tables(self):
        self._set_marquee("Gathering tables from Data Lake...")
        self.window.update()

    def select_lake_table(self, tables,callback):
        self._clear_children(self.body)
        self._clear_children(self.footer_button_box)
        self._set_marquee("Please select the data lake table to be transformed:")
        _locals = {"selecting_table":True}
            
        listbox = Listbox(self.body)
        for i in tables:
            listbox.insert(END, i[0]+'.'+i[1])
        listbox.grid_columnconfigure(0, weight=1)
        listbox.grid_rowconfigure(0, weight=1)

        listbox.grid(row=0, column=0, padx=3,pady=3, sticky='nsew')
        
        def select_table_click():
            callback(listbox.get(listbox.curselection()))    
            _locals['selecting_table'] = False
        
        self.select_table_button = Button(self.footer_button_box, text="select table", command = select_table_click);

        self.select_table_button.grid()
        
        while _locals['selecting_table']:
            self.window.update()
        
    def checking_selection(self):
        self._clear_children(self.body)
        self._clear_children(self.footer_button_box)
        self._set_marquee("Checking your selection and building your repo...")    
        self.window.update()

    def reject_selection(self, existing_model):
        self._set_marquee("Warning: the model {} already exits. Unable to build repo.".format(existing_model))    
        self.window.mainloop()
    
    
    def failed_to_build_new_repo(self):
        self._set_marquee("ERROR: Failed to build new repo")
        self.window.update()

    def getting_table_columns(self,table):
        self._set_marquee("Creating column matrix...")    
        self.window.update()

    def column_matrix(self, columns, callback):
        self._clear_children(self.body)
        self._clear_children(self.footer_button_box)
        self._set_marquee("Select the columns to exclude, set tests, and add comments")    

        _locals = {'setting_up_columns':True}

        matrix = Frame(self.body, background="black")
        matrix.grid_columnconfigure(6, weight=1)
        matrix.grid_rowconfigure(len(columns), weight=1)

        checkbox_vars = dict()
   
        for column in columns:
           checkbox_vars[column] = [IntVar(),IntVar(),IntVar(),StringVar()]

        matrix_header = []
        matrix_header.append(Label(matrix, text = "Column Name"))
        matrix_header.append(Label(matrix, text = "Exclude?"))
        matrix_header.append(Label(matrix, text = "Not Null?"))
        matrix_header.append(Label(matrix, text = "Unique?"))
        matrix_header.append(Label(matrix, text = "Description"))
        
        for index, col in enumerate(matrix_header):
            col.grid(row=0, column=index, sticky="nsew", padx=1,pady=1)        

        for row in range(len(columns)-1):
            current_row = []
            current_row.append(Label(matrix, text = columns[row], borderwidth=0, width= 15))
            current_row.append(Checkbutton(matrix, variable=checkbox_vars[columns[row]][0]))
            current_row.append(Checkbutton(matrix, variable=checkbox_vars[columns[row]][1]))
            current_row.append(Checkbutton(matrix, variable=checkbox_vars[columns[row]][2]))
            current_row.append(Entry(matrix,   textvariable=checkbox_vars[columns[row]][3]))

            for index, r in enumerate(current_row):
                r.grid(row=row + 1,  column=index, sticky="nsew", padx=1,pady=1)

        matrix.grid(column=0,row=0, padx=1, pady=1)
        
        def submit_columns():
            finalized_input_values = dict()
            for col, values in checkbox_vars.items():
                finalized_input_values[col] = []
                for val in values:
                    finalized_input_values[col].append(val.get())

            callback(finalized_input_values)
            _locals['setting_up_columns'] = False        

        set_columns_button = Button(self.footer_button_box, text= "Create Models", command = submit_columns)
        set_columns_button.grid(row=12, column= 8)

        while _locals['setting_up_columns']:
            self.window.update()
        

    def select_model_group(self, model_groups,callback):
        self._clear_children(self.body)
        self._clear_children(self.footer_button_box)
        self._set_marquee("Select the parent model grouping for the new table")    

        _locals = {"selecting_model_group":True}
            
        
        listbox = Listbox(self.body)
        for i in model_groups:
            listbox.insert(END, i)
        listbox.grid_columnconfigure(0, weight=1)
        listbox.grid_rowconfigure(0, weight=1)

        listbox.grid(row=0, column=0, padx=3,pady=3, sticky='nsew')
        
        def select_grouping_click():
            callback(listbox.get(listbox.curselection()))    
            _locals['selecting_model_group'] = False

        select_grouping_button = Button(self.footer_button_box, text= "Select Model Group", command = select_grouping_click)
        select_grouping_button.grid()
        
        while _locals['selecting_model_group']:
            self.window.update()

    def generating_models_and_tests(self):
        self._clear_children(self.body)
        self._clear_children(self.footer_button_box)
        self._set_marquee("Generating dbt models and populating schema tests...")    
        self.window.update()

    def committing_and_pushing(self):
        self._clear_children(self.body)
        self._clear_children(self.footer_button_box)
        self._set_marquee("Commiting work and pushing to origin...")    
        self.window.update()

    def commit_failed(self):
        self._clear_children(self.body)
        self._clear_children(self.footer_button_box)
        self._set_marquee("Commit/Push FAILED!!")    
        self.window.update()

    def completed(self):
        self._clear_children(self.body)
        self._clear_children(self.footer_button_box)
        self._set_marquee('')    

        completed_text = Label(self.body, text = "Completed! You can view your branch on GitHub and create a pull reqeust.")
        completed_text.grid(column=0, row=0, sticky='nsew')

        def exit_click():
            sys.exit()

        exit_button = Button(self.footer_button_box, text= "Finish", command = exit_click)
        exit_button.grid()
        
        self.window.mainloop()


