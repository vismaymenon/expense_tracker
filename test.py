import tkinter as tk

root = tk.Tk()
root.title("Grid Splitting Example")

# Create some widgets for the initial grid
label1 = tk.Label(root, text="Label 1", borderwidth=2, relief="solid")
label2 = tk.Label(root, text="Label 2", borderwidth=2, relief="solid")
button1 = tk.Button(root, text="Button 1", borderwidth=2, relief="solid")
button2 = tk.Button(root, text="Button 2", borderwidth=2, relief="solid")

# Place them in the grid
label1.grid(row=0, column=0)
label2.grid(row=0, column=1)
button1.grid(row=1, column=0)
button2.grid(row=1, column=1)

# Function to split the cell at row 0, column 0
def split_cell():
    label1.grid_remove()

    # Create new labels for the split cell
    new_label1 = tk.Label(root, text="New Label 1", borderwidth=2, relief="solid")
    new_label2 = tk.Label(root, text="New Label 2", borderwidth=2, relief="solid")

    # Place the new labels in the split cell area
    new_label1.grid(row=0, column=0, padx=5, pady=5)
    new_label2.grid(row=0, column=1, padx=5, pady=5)

# Create a button to trigger the split
split_button = tk.Button(root, text="Split Cell", command=split_cell)
split_button.grid(row=2, column=0, columnspan=2)  # Span across both columns

root.mainloop()