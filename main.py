import customtkinter as ctk

ctk.set_appearance_mode('System')
ctk.set_default_color_theme('blue')

class ExpenseTrackerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('Expense Tracker')
        self.geometry('600x400')

        #Column configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        # Row configuration
        self.grid_rowconfigure(0, weight=1)

        # coulmn 0
        self.column0_frame = ExpensesListFrame(self)
        self.column0_frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)


        # Column 1
        ## Add Expense Button
        self.add_expense_button = ctk.CTkButton(self, text='Add Expense', command=self.open_add_expense, width=80, height=28)
        self.add_expense_button.grid(row=0, column=1, padx=10, pady=(10,0), sticky='nw')
        self.add_expense_window = None
    def open_add_expense(self):
        if self.add_expense_window is None or not self.add_expense_window.winfo_exists():
            self.add_expense_window = AddExpenseWindow(self)
        else:
            self.add_expense_window.focus()
class AddExpenseWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('Add Expense')
        self.geometry('250x300')
        for i in range(6):  # for columns 0, 1, 2
            self.grid_rowconfigure(i, weight=1)
        self.grid_columnconfigure(0, weight=1)
        # Title Label
        self.title_label = ctk.CTkLabel(self, text= 'Add Your Expenses', font=("Arial", 24))
        self.title_label.grid(row= 0,column=0, sticky = 'w', padx = 10, pady = 10)
        #entries
        self.add_amount = ctk.CTkEntry(self, placeholder_text= 'Amount')
        self.add_amount.grid(row=1, column=0, padx=10, pady=(0, 10), sticky='ew')
        self.add_category = ctk.CTkEntry(self, placeholder_text='Category')
        self.add_category.grid(row=2, column=0, padx=10, pady=(0, 10), sticky='ew')
        self.add_description = ctk.CTkEntry(self, placeholder_text='Description (Optional)')
        self.add_description.grid(row=3, column=0, padx=10, pady=(0, 10), sticky='ew')
        # Add Button
        self.add_button = ctk.CTkButton(self, text="Submit", command=self.submit_add_expense)
        self.add_button.grid(row = 4, column = 0, padx= 10, pady=(0,10), sticky = 'ew')
        # Feedback Label
        self.feedback_label = ctk.CTkLabel(self, text="")
        self.feedback_label.grid(row = 5, column = 0, padx= 10, pady=(0,10), sticky = 'ew')
    def submit_add_expense(self):
        amount = self.add_amount.get()
        category = self.add_category.get()
        description = self.add_description.get()

        if amount and category:
            self.feedback_label.configure(text=f"Added: ${amount} - {category}")
            # In the future: Save to CSV or DB
        else:
            self.feedback_label.configure(text="Please enter at least amount and category.")

class ExpensesListFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(border_width=3, border_color='steelblue2')
        #Row Configuration
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        # Column Configuration
        self.grid_columnconfigure(0, weight=1)

        # title
        self.title = ctk.CTkLabel(self, text="Expense Tracker", font=("Arial", 24, "underline"), underline=True)
        self.title.grid(row=0, column=0, sticky='nw', padx=10, pady=10)
        # View options
        self.view_options = ViewButtons(self, options = ['Daily', 'Weekly', 'Monthly', 'Yearly'])
        self.view_options.grid(row=0, column=0, sticky='new', padx=10, pady=(50, 10))

class ViewButtons(ctk.CTkFrame):
    def __init__(self, master, options):
        super().__init__(master, fg_color='transparent')
        self.grid_rowconfigure(0, weight=1)
        for i in range(len(options)):
            self.grid_columnconfigure(i, weight=1)
        self.buttons = []
        for i, option in enumerate(options):
            button = ctk.CTkButton(
                self,
                text=option,
                width=80,
                height=28,
                command=lambda idx=i: self.set_active_view(idx)
                #index based command, 0:daily, 1:weekly, 2:monthly, 3:yearly
            )
            button.grid(row=0, column=i, padx=5, pady=5)
            self.buttons.append(button)
        self.buttons[0].configure(fg_color='steelblue4')
        self.active_index = 0  # Default to first button
        self.set_active_view(0)

    def set_active_view(self, idx):
        for i, btn in enumerate(self.buttons):
            btn.configure(fg_color='steelblue4' if i == idx else 'steelblue2')

    def get_active_view(self):
        return self.buttons[self.active_index].cget('text')

if __name__ == "__main__":
    app = ExpenseTrackerApp()
    app.mainloop()