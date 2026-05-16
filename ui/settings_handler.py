import customtkinter as ctk
from customtkinter import CTkLabel


class SettingsFrame(ctk.CTkFrame):
    def __init__(self, parent, configs, accounts):
        super().__init__(parent, fg_color="#FFFFFF", border_color="#E0E0E0", border_width=3, height=400, width=600)

        self.closeBtn = CTkLabel(self,text="x", text_color="#111111",fg_color="#FFFFFF",font=("Segoe UI",15))
        self.closeBtn.place(x=585,y=5,anchor="ne")
        self.closeBtn.bind("<Button-1>", self.close_self)

    def open_self(self):
        root = self.winfo_toplevel()
        w = root.winfo_width()
        h = root.winfo_height()
        self.place(x=w // 2, y=h // 2, anchor="center")
        self.lift()

    def close_self(self,event=None):
        self.place_forget()