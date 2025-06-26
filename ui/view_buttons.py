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

class ViewButtons(ctk.CTkTabview):
    def __init__(self, master, options):
        super().__init__(master, fg_color='transparent')
        self.grid_rowconfigure(0, weight=1)


    def set_active_view(self, idx):
        for i, button in enumerate(self.buttons):
            if i == idx:
                button.configure(fg_color='steelblue4')
            else:
                button.configure(fg_color='steelblue2')
        self.active_index = idx
