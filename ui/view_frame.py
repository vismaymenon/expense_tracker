import customtkinter as ctk
from tkinter import ttk
from data.data_manager import DataManager

class ViewFrame(ctk.CTkTabview):
    def __init__(self, master, options, data_manager):
        super().__init__(master)
        for i in range(len(options)):
            self.add(options[i])
        self.data_manager = data_manager


        #Expenses List_Daily
        self.scrollable_frame = ctk.CTkScrollableFrame(self.tab('Daily'), label_text="Transactions")
        self.scrollable_frame.pack(fill='both', expand=True, padx=10, pady=10)
        # Populate the list on startup
        self.populate_expenses()

        # # Column 1
        # # Frame for pie chart data analysis
        # self.pie_chart_frame = ctk.CTkFrame(self.scrollable_frame, fg_color='red')
        # self.pie_chart_frame.grid(row=0, column=1, sticky='nsew', padx=10, pady=(10, 10))

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