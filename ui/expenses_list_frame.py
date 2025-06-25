import customtkinter as ctk

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
            )
            button.grid(row=0, column=i, padx=5, pady=5, sticky='ew')
            self.buttons.append(button)
        self.active_index = 0
        self.set_active_view(0)

    def set_active_view(self, idx):
        for i, button in enumerate(self.buttons):
            if i == idx:
                button.configure(fg_color='steelblue4')
            else:
                button.configure(fg_color='steelblue2')
        self.active_index = idx

class ExpensesListFrame(ctk.CTkFrame):
    def __init__(self, master, data_manager):
        super().__init__(master)
        self.data_manager = data_manager
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
        # Expenses List
        self.scrollable_frame = ctk.CTkScrollableFrame(self, label_text="Transactions")
        self.scrollable_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)
        self.grid_rowconfigure(1, weight=10)  # Give more weight to the list
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
            sign = "+" if entry['type'] == 'Income' else "-"

            label_text = f"{entry['date']}: {entry['category']} ({entry['description']})"
            amount_text = f"{sign}${float(entry['amount']):.2f}"

            ctk.CTkLabel(entry_frame, text=label_text).pack(side='left', padx=10)
            ctk.CTkLabel(entry_frame, text=amount_text, text_color=amount_color).pack(side='right', padx=10)