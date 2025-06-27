# import customtkinter as ctk
# from tkinter import ttk
# from data.data_manager import DataManager
#
# class ViewFrame(ctk.CTkTabview):
#     def __init__(self, master, options, data_manager):
#         super().__init__(master)
#         for i in range(len(options)):
#             self.add(options[i])
#         self.data_manager = data_manager
#
#
#         #Expenses List_Daily
#         self.scrollable_frame = ctk.CTkScrollableFrame(self.tab('Daily'), label_text="Transactions")
#         self.scrollable_frame.pack(fill='both', expand=True, padx=10, pady=10)
#         # Populate the list on startup
#         self.populate_expenses()
#
#         # # Column 1
#         # # Frame for pie chart data analysis
#         # self.pie_chart_frame = ctk.CTkFrame(self.scrollable_frame, fg_color='red')
#         # self.pie_chart_frame.grid(row=0, column=1, sticky='nsew', padx=10, pady=(10, 10))
#
#     def populate_expenses(self):
#         # Clear any existing widgets
#         for widget in self.scrollable_frame.winfo_children():
#             widget.destroy()
#
#         entries = self.data_manager.get_all_entries()
#         # Display in reverse order (newest first)
#         for i, entry in enumerate(reversed(entries)):
#             entry_frame = ctk.CTkFrame(self.scrollable_frame)
#             entry_frame.grid(row = 0, column = 0, sticky='nsew', padx=10, pady=(5, 5))
#
#             # Determine color based on type
#             amount_color = "light green" if entry['type'] == 'Income' else "light coral"
#             if entry['description']:
#                 label_text = f"{entry['date']}: {entry['category']} ({entry['description']})"
#             else:
#                 label_text = f"{entry['date']}: {entry['category']}"
#             amount_text = f"${float(entry['amount']):.2f}"
#
#             ctk.CTkLabel(entry_frame, text=label_text).pack(side='left', padx=10)
#             ctk.CTkLabel(entry_frame, text=amount_text, text_color=amount_color).pack(side='right', padx=10)


import customtkinter as ctk
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Define colors for the app
BG_COLOR = "#242424"  # Default CTk dark background
ALT_ROW_COLOR = "#2B2B2B"
TEXT_COLOR = "#DCE4EE"
INCOME_COLOR = "#00A968"
EXPENSE_COLOR = "#FF5757"


class ExpenseGroupFrame(ctk.CTkFrame):
    """A frame that displays transactions for a single group (e.g., one day),
       including a details list, a pie chart, and a net flow summary."""

    def __init__(self, master, group_date_str, group_df):
        super().__init__(master, fg_color="transparent")
        self.group_date_str = group_date_str
        self.group_df = group_df

        self.grid_columnconfigure(0, weight=3)  # Give more space to the list
        self.grid_columnconfigure(1, weight=2)  # Space for the chart
        # --- FIX APPLIED HERE ---
        # This allows the content row (row 1) to expand vertically,
        # ensuring the frame calculates its total required height correctly.
        self.grid_rowconfigure(1, weight=1)

        # --- Title for the group ---
        title_label = ctk.CTkLabel(self, text=self.group_date_str, font=ctk.CTkFont(size=16, weight="bold"))
        title_label.grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=(5, 10))

        # --- Left Column: Transaction List ---
        self.create_transaction_list()

        # --- Right Column: Analysis (Pie Chart & Net Flow) ---
        self.create_analysis_section()

    def create_transaction_list(self):
        list_frame = ctk.CTkFrame(self, fg_color="transparent")
        list_frame.grid(row=1, column=0, sticky="nsew", padx=10)

        for i, row in enumerate(self.group_df.iterrows()):
            entry = row[1]
            # Alternating row colors
            row_color = "transparent" if i % 2 == 0 else ALT_ROW_COLOR

            row_frame = ctk.CTkFrame(list_frame, fg_color=row_color)
            row_frame.pack(fill="x", pady=1)

            # Description and Category
            desc_text = entry['category']
            if pd.notna(entry['description']) and entry['description'] != '':
                desc_text += f" ({entry['description']})"

            label = ctk.CTkLabel(row_frame, text=desc_text, anchor="w")
            label.pack(side="left", fill="x", expand=True, padx=5, pady=2)

            # Amount
            amount_color = INCOME_COLOR if entry['type'] == 'Income' else TEXT_COLOR
            amount_text = f"${abs(entry['amount']):,.2f}"
            amount_label = ctk.CTkLabel(row_frame, text=amount_text, text_color=amount_color, anchor="e", width=100)
            amount_label.pack(side="right", padx=5, pady=2)

    def create_analysis_section(self):
        analysis_frame = ctk.CTkFrame(self, fg_color="transparent")
        analysis_frame.grid(row=1, column=1, sticky="nsew", padx=10)
        analysis_frame.grid_rowconfigure(0, weight=1)  # Pie chart takes up space
        analysis_frame.grid_rowconfigure(1, weight=0)  # Net flow is fixed size

        # --- Pie Chart ---
        expenses_only_df = self.group_df[self.group_df['type'] == 'Expense'].copy()

        fig_frame = ctk.CTkFrame(analysis_frame, fg_color="transparent")
        fig_frame.grid(row=0, column=0, sticky="nsew")

        if not expenses_only_df.empty:
            category_summary = expenses_only_df.groupby('category')['amount'].sum().abs()

            fig = Figure(figsize=(5, 4), dpi=100)
            fig.patch.set_facecolor(BG_COLOR)  # Match background
            ax = fig.add_subplot(111)
            ax.pie(category_summary, labels=category_summary.index, autopct='%1.1f%%',
                   startangle=90, textprops={'color': TEXT_COLOR})
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            fig.tight_layout()

            canvas = FigureCanvasTkAgg(fig, master=fig_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side="top", fill="both", expand=True)
        else:
            no_data_label = ctk.CTkLabel(fig_frame, text="No expenses to display", text_color="gray")
            no_data_label.pack(expand=True, padx=5, pady=5)

        # --- Net Flow ---
        net_flow = self.group_df['amount'].sum()
        net_flow_color = INCOME_COLOR if net_flow >= 0 else EXPENSE_COLOR
        net_flow_text = f"Net Flow: ${net_flow:,.2f}"

        net_flow_label = ctk.CTkLabel(analysis_frame, text=net_flow_text, text_color=net_flow_color,
                                      font=ctk.CTkFont(size=14, weight="bold"))
        net_flow_label.grid(row=1, column=0, sticky="ew", pady=(10, 5))


class ViewFrame(ctk.CTkTabview):
    def __init__(self, master, options, data_manager):
        super().__init__(master, fg_color=BG_COLOR)
        self.options = options
        self.data_manager = data_manager

        # Add tabs
        for option in options:
            self.add(option)
            # Create a scrollable frame inside each tab
            scroll_frame = ctk.CTkScrollableFrame(self.tab(option), label_text=f"{option} View")
            scroll_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.populate_all_tabs()

        # Bind the tab change event to refresh data
        self.configure(command=self.populate_all_tabs)

    def populate_all_tabs(self):
        """Populates the currently selected tab with grouped data."""
        selected_tab_name = self.get()

        # Updated 'M' to 'ME' and 'Y' to 'YE' to resolve FutureWarning
        period_map = {'Daily': 'D', 'Weekly': 'W', 'Monthly': 'ME', 'Yearly': 'YE'}

        if selected_tab_name not in period_map:
            return

        period_code = period_map[selected_tab_name]
        grouped_entries = self.data_manager.get_grouped_entries(period_code)

        # Get the correct scrollable frame for the current tab
        tab_frame = self.tab(selected_tab_name)
        scroll_frame = tab_frame.winfo_children()[0]  # Assumes scroll frame is the only child

        # Clear previous content
        for widget in scroll_frame.winfo_children():
            widget.destroy()

        if grouped_entries.ngroups == 0:
            no_data_label = ctk.CTkLabel(scroll_frame, text="No transactions for this period.")
            no_data_label.pack(expand=True, pady=20)
            return

        # Create a group frame for each period with data
        for group_date, group_df in grouped_entries:
            if not group_df.empty:
                # Format the date string for display
                if period_code == 'D':
                    date_str = group_date.strftime('%A, %d %B %Y')
                elif period_code == 'W':
                    start_date = group_date.strftime('%d %b')
                    end_date = (group_date + pd.Timedelta(days=6)).strftime('%d %b %Y')
                    date_str = f"Week of {start_date} to {end_date}"
                elif period_code == 'ME':
                    date_str = group_date.strftime('%B %Y')
                elif period_code == 'YE':
                    date_str = group_date.strftime('%Y')

                group_frame = ExpenseGroupFrame(scroll_frame, date_str, group_df)
                group_frame.pack(fill='x', padx=5, pady=10)
