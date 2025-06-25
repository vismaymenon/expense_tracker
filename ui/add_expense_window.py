import customtkinter as ctk

class AddExpenseWindow(ctk.CTkToplevel):
    def __init__(self,master, *args, **kwargs):
        super().__init__(master,*args, **kwargs)
        self.master_app = master
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
            # For now, let's assume everything is an 'Expense'.
            # can add a CTkSegmentedButton later to choose between Expense/Income.
            self.master_app.data_manager.add_entry('Expense', category, description, amount)
            self.feedback_label.configure(text=f"Added: ${amount} - {category}", text_color="green")
            # Tell the main app to refresh its view
            self.master_app.expense_added()
            # Clear fields after successful submission
            self.add_amount.delete(0, 'end')
            self.add_category.delete(0, 'end')
            self.add_description.delete(0, 'end')
        else:
            self.feedback_label.configure(text="Amount and Category are required.", text_color="red")

