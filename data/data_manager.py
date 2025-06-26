import csv
import os
from datetime import datetime

class DataManager:
    def __init__(self, filename='expenses.csv'):
        self.filename = filename
        self.fieldnames = ['date', 'type', 'category', 'description', 'amount']
        # Create the file with a header if it doesn't exist
        if not os.path.exists(self.filename):
            with open(self.filename, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
                writer.writeheader()

    def add_entry(self,entry_date, entry_type, category, description, amount):
        # Basic validation
        try:
            if entry_type == 'Expense':
                amount_float = -float(amount)
            else:
                amount_float = float(amount)
        except ValueError:
            print("Error: Amount must be a number.")
            return

        with open(self.filename, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
            writer.writerow({
                'date': datetime.strptime(entry_date, '%Y-%m-%d').strftime('%Y-%m-%d'),
                'type': entry_type,
                'category': category,
                'description': description,
                'amount': amount_float
            })

    def get_all_entries(self):
        with open(self.filename, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            return list(reader)