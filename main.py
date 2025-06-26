import customtkinter as ctk
import tkinter as tk
from ui.add_expense_window import AddExpenseWindow
from ui.expenses_list_frame import ExpensesListFrame
from data.data_manager import DataManager

ctk.set_appearance_mode('System')
ctk.set_default_color_theme('blue')

class ExpenseTrackerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('Expense Tracker')
        self.geometry('800x600')
        self.data_manager = DataManager()
        #Column configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        # -------------------Courtesy of Gemini-------------------------------------------------
        # --- THE FIX FOR THE MAIN WINDOW MACOS FOCUS ISSUE ---
        # These lines ensure the main window itself gets proper initial focus
        # after it's fully rendered by the OS.
        self.lift()  # Bring the window to the front
        self.attributes("-topmost", True)  # Temporarily make it stay on top
        self.after(50, self.focus_force)  # Force focus to the window after a tiny delay

        # Important: Remove the "-topmost" attribute after a short delay.
        # You generally don't want your main app window to always be on top
        # of *other applications* on your desktop. We only need it for initial focus.
        self.after(150, lambda: self.attributes("-topmost", False))
        # --------------------------------------------------------------------

        # Row configuration
        self.grid_rowconfigure(0, weight=1)

        # coulmn 0
        self.column0_frame = ExpensesListFrame(self, data_manager = self.data_manager)
        self.column0_frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)


        # Column 1
        ## Add Expense Button
        self.add_expense_button = ctk.CTkButton(self, text='Add Expense', command=self.open_add_expense, width=80, height=28)
        self.add_expense_button.grid(row=0, column=1, padx=10, pady=(10,0), sticky='nw')
        self.add_expense_window = None

    def open_add_expense(self):
        if self.add_expense_window is None or not self.add_expense_window.winfo_exists():
            self.add_expense_window = AddExpenseWindow(self)
            self.add_expense_window.transient(self)
        else:
            self.add_expense_window.lift()
            self.add_expense_window.focus_force()
    def expense_added(self):
        """This function will be called to refresh the list"""
        self.column0_frame.populate_expenses()

if __name__ == "__main__":
    app = ExpenseTrackerApp()
    app.mainloop()