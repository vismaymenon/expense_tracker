import customtkinter as ctk
import tkinter as tk

root = ctk.CTk()
root.title("CTkEntry Text Variable Example")

# Create a StringVar
entry_text_var = tk.StringVar()

# Create a CTkEntry and link it to the StringVar
entry_widget = ctk.CTkEntry(master=root, textvariable=entry_text_var, placeholder_text="Enter text here")
entry_widget.pack(pady=20)

# Set initial text
entry_text_var.set("Initial Value")

# Function to get and print the current text
def print_entry_text():
    print(f"Current text: {entry_text_var.get()}")

# Button to trigger printing the text
get_text_button = ctk.CTkButton(master=root, text="Get Text", command=print_entry_text)
get_text_button.pack()

root.mainloop()