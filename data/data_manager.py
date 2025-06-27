import pandas as pd
import os
from datetime import datetime


class DataManager:
    def __init__(self, filename='expenses.csv'):
        self.filename = filename
        self.fieldnames = ['date', 'type', 'category', 'description', 'amount']
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Creates the CSV with a header if it doesn't exist."""
        if not os.path.exists(self.filename):
            with open(self.filename, 'w', newline='') as csvfile:
                writer = pd.DataFrame(columns=self.fieldnames)
                writer.to_csv(self.filename, index=False)

    def add_entry(self, entry_date, entry_type, category, description, amount):
        """Adds a single new entry to the CSV file."""
        try:
            # Store expenses as negative numbers for easy summation
            amount_float = -float(amount) if entry_type == 'Expense' else float(amount)
        except ValueError:
            print("Error: Amount must be a number.")
            return

        new_entry = pd.DataFrame([{
            'date': datetime.strptime(entry_date, '%Y-%m-%d').strftime('%Y-%m-%d'),
            'type': entry_type,
            'category': category,
            'description': description,
            'amount': amount_float
        }])

        new_entry.to_csv(self.filename, mode='a', header=False, index=False)

    def get_entries_as_dataframe(self):
        """Reads all entries from the CSV and returns them as a pandas DataFrame."""
        if not os.path.exists(self.filename) or os.path.getsize(self.filename) == 0:
            return pd.DataFrame(columns=self.fieldnames)

        try:
            df = pd.read_csv(self.filename)
            # Convert 'date' column to datetime objects for proper sorting and grouping
            df['date'] = pd.to_datetime(df['date'])
            # Ensure amount is numeric
            df['amount'] = pd.to_numeric(df['amount'])
            return df
        except pd.errors.EmptyDataError:
            return pd.DataFrame(columns=self.fieldnames)

    def get_grouped_entries(self, period):
        """
        Groups entries by a given time period.
        :param period: One of 'D' (Day), 'W' (Week), 'M' (Month), 'Y' (Year)
        :return: A pandas DataFrameGroupBy object
        """
        df = self.get_entries_as_dataframe()
        if df.empty:
            return df.groupby(pd.Grouper(key='date', freq=period))

        # We group by the 'date' column using a specific frequency
        # W-MON means weeks start on Monday.
        return df.sort_values('date', ascending=False).groupby(
            pd.Grouper(key='date', freq=period if period != 'W' else 'W-MON'))