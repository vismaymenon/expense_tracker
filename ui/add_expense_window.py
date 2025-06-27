import datetime
import tkinter as tk
import customtkinter as ctk
from ui.view_frame import ViewFrame

class AddExpenseWindow(ctk.CTkToplevel):
    def __init__(self,master, *args, **kwargs):
        super().__init__(master,*args, **kwargs)
        self.master_app = master
        self.title('Add Expense')
        self.geometry('350x400')
        self.protocol("WM_DELETE_WINDOW", self._on_closing)
        # --------------------------------------------------------------------
        # --- THE FIX FOR THE MACOS FOCUS & CLICK ISSUE ---
        # --------------------------------------------------------------------
        self.lift()  # Raise this window to the top of the stacking order.
        self.attributes("-topmost", True)  # Ensure it stays on top of the main window.
        self.grab_set()  # Make the window modal (as discussed before, this is good practice).

        # This is the most important line for the fix.
        # It waits 10ms for the window to draw, then forces focus to it.
        self.after(10, self.focus_force)
        # --------------------------------------------------------------------
        # Title Label
        self.title_label = ctk.CTkLabel(self, text= 'Add Your Expenses', font=("Arial", 24))
        self.title_label.pack(side = 'top', padx = 10, pady = 10)
        #Income or Expense Segmented Button
        self.income_or_expense = ctk.CTkSegmentedButton(self, values = ['Expense', 'Income'])
        self.income_or_expense.set('Expense')
        self.income_or_expense.pack(padx=10, pady=(0, 10), fill='x', expand=True)
        # Date Entry
        self.current_date_var = tk.StringVar()
        self.date_entry = ctk.CTkEntry(self, textvariable= self.current_date_var, width=200)
        self.current_date_var.set(datetime.datetime.now().strftime('%Y-%m-%d'))
        self.date_entry.pack(padx=10, pady=(0, 10), fill = 'x', expand = True)
        # Amount, Category, Description Entries
        self.add_amount = ctk.CTkEntry(self, placeholder_text= 'Amount')
        self.add_amount.pack(padx=10, pady=(0, 10), fill = 'x', expand = True)
        self.add_category = ctk.CTkEntry(self, placeholder_text='Category')
        self.add_category.pack(padx=10, pady=(0, 10), fill = 'x', expand = True)
        self.add_description = ctk.CTkEntry(self, placeholder_text='Description (Optional)')
        self.add_description.pack(padx=10, pady=(0, 10), fill = 'x', expand = True)
        # Add Button
        self.add_button = ctk.CTkButton(self, text="Submit", command=self.submit_add_expense)
        self.add_button.pack(padx= 10, pady=(0,10), fill = 'x', expand = True)
        # Feedback Label
        self.feedback_label = ctk.CTkLabel(self, text="")
        self.feedback_label.pack(padx= 10, pady=(0,10), fill = 'x', expand = True)
    def submit_add_expense(self):
        transaction_type = self.income_or_expense.get()
        entry_date = self.current_date_var.get()
        amount = self.add_amount.get()
        category = self.add_category.get()
        description = self.add_description.get()

        if entry_date and amount and category:
            # For now, let's assume everything is an 'Expense'.
            # can add a CTkSegmentedButton later to choose between Expense/Income.
            self.master_app.data_manager.add_entry(entry_date,transaction_type, category, description, amount)
            self.feedback_label.configure(text=f"Added: ${amount} - {category}", text_color="green")
            # Tell the main app to refresh its view
            self.master_app.expense_added()
            # Clear fields after successful submission
            self.add_amount.delete(0, 'end')
            self.add_category.delete(0, 'end')
            self.add_description.delete(0, 'end')
        else:
            self.feedback_label.configure(text="Date, Amount and Category are required.", text_color="red")

    def _on_closing(self):
        self.grab_release()
        if self.master_app and self.master_app.winfo_exists():
            self.master_app.focus_force()
        self.after(10, self.destroy)  # Ensure the window is destroyed after a short delay

    def expense_added(self):
        """This function will be called to refresh the list"""
        ViewFrame.populate_all_tabs()