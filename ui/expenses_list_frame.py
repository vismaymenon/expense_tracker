import customtkinter as ctk
from ui.add_expense_window import AddExpenseWindow
from ui.view_buttons import ViewButtons

class ExpensesListFrame(ctk.CTkFrame):
    def __init__(self, master, data_manager):
        super().__init__(master)
        self.data_manager = data_manager
        self.configure(border_width=3, border_color='steelblue2')
        #Row Configuration
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=10) # Give more weight to the list
        # Column Configuration
        self.grid_columnconfigure(0, weight=1)

        # title frame
        self.title_frame = ctk.CTkFrame(self, fg_color='transparent')
        self.title_frame.grid_columnconfigure(0, weight=1)
        self.title_frame.grid_columnconfigure(1, weight=1)  # Button column
        self.title_frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
        self.title = ctk.CTkLabel(self.title_frame, text="Expense Tracker", font=("Arial", 24, "underline"), underline=True)
        self.title.grid(row=0, column=0, sticky='nw', padx=10, pady=10)
        # Add Expense Button to the title frame
        self.add_expense_button = ctk.CTkButton(self.title_frame, text='Add Expense', command=self.open_add_expense, width=50, height=30)
        self.add_expense_button.grid(row=0, column=1, padx=5, pady=5, sticky='e')
        self.add_expense_window = None

        # View Options Frame
        self.view_options_frame = ctk.CTkFrame(self, fg_color='transparent')
        self.view_options_frame.grid(row=1, column=0, sticky='nsew', padx=0, pady=0)
        # View options
        self.view_options = ViewButtons(self.view_options_frame, options = ['Daily', 'Weekly', 'Monthly', 'Yearly'])
        self.view_options.grid(row=0, column=0, sticky='new', padx=10, pady=(50, 10))
        # Expenses List
        self.scrollable_frame = ctk.CTkScrollableFrame(self, label_text="Transactions")
        self.scrollable_frame.grid(row=2, column=0, sticky='nsew', padx=10, pady=10)
        # Populate the list on startup
        self.populate_expenses()



    def populate_expenses(self):
        # Clear any existing widgets
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        entries = self.data_manager.get_all_entries()
        # Display in reverse order (newest first)
        for i, entry in enumerate(reversed(entries)):
            entry_frame = ctk.CTkFrame(self.scrollable_frame)
            entry_frame.pack(fill='x', padx=5, pady=5)

            # Determine color based on type
            amount_color = "light green" if entry['type'] == 'Income' else "light coral"
            if entry['description']:
                label_text = f"{entry['date']}: {entry['category']} ({entry['description']})"
            else:
                label_text = f"{entry['date']}: {entry['category']}"
            amount_text = f"${float(entry['amount']):.2f}"

            ctk.CTkLabel(entry_frame, text=label_text).pack(side='left', padx=10)
            ctk.CTkLabel(entry_frame, text=amount_text, text_color=amount_color).pack(side='right', padx=10)

    def open_add_expense(self):
        if self.add_expense_window is None or not self.add_expense_window.winfo_exists():
            self.add_expense_window = AddExpenseWindow(self)
            self.add_expense_window.transient(self.winfo_toplevel())  # Set the parent window
        else:
            self.add_expense_window.lift()
            self.add_expense_window.focus_force()
    def expense_added(self):
        """This function will be called to refresh the list"""
        self.populate_expenses()