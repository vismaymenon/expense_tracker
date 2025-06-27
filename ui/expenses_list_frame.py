import customtkinter as ctk
from ui.add_expense_window import AddExpenseWindow
from ui.view_frame import ViewFrame

class ExpensesListFrame(ctk.CTkFrame):
    def __init__(self, master, data_manager):
        super().__init__(master)
        self.configure(border_width=3, border_color='steelblue2')
        self.data_manager = data_manager
        #Row Configuration
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=10) # Give more weight to the list
        # Column Configuration
        self.grid_columnconfigure(0, weight=1)

        #Row 0: Title and Add Expense Button
        # title frame
        self.title_frame = ctk.CTkFrame(self)
        self.title_frame.grid_columnconfigure(0, weight=1)
        self.title_frame.grid_columnconfigure(1, weight=1)  # Button column
        self.title_frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
        self.title = ctk.CTkLabel(self.title_frame, text="Expense Tracker", font=("Arial", 24, "underline"), underline=True)
        self.title.grid(row=0, column=0, sticky='nw', padx=10, pady=10)
        # Add Expense Button to the title frame
        self.add_expense_button = ctk.CTkButton(self.title_frame, text='Add Expense', command=self.open_add_expense, width=50, height=30)
        self.add_expense_button.grid(row=0, column=1, padx=5, pady=5, sticky='e')
        self.add_expense_window = None

        #Row 1: View Options and Expenses List
        # View options
        self.view_options = ViewFrame(self, options = ['Daily', 'Weekly', 'Monthly', 'Yearly'], data_manager=self.data_manager)
        self.view_options.grid(row=1, column=0, sticky='nsew', padx=10, pady=(0, 10))


    def open_add_expense(self):
        if self.add_expense_window is None or not self.add_expense_window.winfo_exists():
            self.add_expense_window = AddExpenseWindow(self)
            self.add_expense_window.transient(self.winfo_toplevel())  # Set the parent window
        else:
            self.add_expense_window.lift()
            self.add_expense_window.focus_force()
