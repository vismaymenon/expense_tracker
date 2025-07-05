import customtkinter as ctk
import tkinter as tk
from ui.expenses_list_frame import ExpensesListFrame
from ui.news_frame import NewsFrame
from data.data_manager import DataManager

ctk.set_appearance_mode('System')
ctk.set_default_color_theme('blue')

class ExpenseTrackerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('Expense Tracker')
        self.geometry('1200x800')
        self.data_manager = DataManager()
        #Column configuration
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=1)
        #row configuration
        self.grid_rowconfigure(0, weight=1)
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

        # Column 0
        self.column0_frame = ExpensesListFrame(self, data_manager = self.data_manager)
        self.column0_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=10)

        # Column 1
        self.column1_frame = NewsFrame(self)
        self.column1_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=10)


if __name__ == "__main__":
    app = ExpenseTrackerApp()
    app.mainloop()