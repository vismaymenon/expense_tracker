import customtkinter as ctk

class NewsFrame(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master, label_text="News and Updates")
        # self.pack(fill='both', expand=True, padx=10, pady=10)

        # Example news items
        self.news_items = [
            "Version 1.0 released!",
            "New features coming soon.",
            "Bug fixes and performance improvements.",
            "Check out our new documentation."
        ]

        #self.populate_news()

