import customtkinter as ctk

app = ctk.CTk()
app.geometry("500x400")

tabview = ctk.CTkTabview(master=app)
tabview.pack(padx=20, pady=20)

tabview.add("Tab 1")
tabview.add("Tab 2")

scrollable_frame_1 = ctk.CTkScrollableFrame(master=tabview.tab("Tab 1"), label_text="Scrollable Frame in Tab 1")
scrollable_frame_1.pack(padx=10, pady=10)

scrollable_frame_2 = ctk.CTkScrollableFrame(master=tabview.tab("Tab 2"), label_text="Scrollable Frame in Tab 2")
scrollable_frame_2.pack(padx=10, pady=10)


for i in range(20):
    ctk.CTkButton(master=scrollable_frame_1, text=f"Button {i+1}").pack(pady=5)
    ctk.CTkButton(master=scrollable_frame_2, text=f"Button {i+1}").pack(pady=5)


print(tabview.tab("Tab 1").winfo_children()[0].winfo_children()[0].winfo_children())
app.mainloop()