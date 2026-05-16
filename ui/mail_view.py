import customtkinter as ctk
from customtkinter import CTkFrame, CTkButton, CTkLabel, CTkScrollableFrame

class MailView(ctk.CTkFrame):
    def __init__(self, parent, imap, smtp, configs):
        super().__init__(parent,fg_color="#FFFFFF",corner_radius=0, height=700,width= 400,border_width=2,border_color="#f0f0f0")

        self.imap = imap
        self.smtp = smtp
        self.configs = configs

        self.ml = MailRead(parent, self.imap)
        self.ml.place(x=420, y=70, anchor="nw")

        self.mr = MailWrite(parent, self.smtp, self.configs)



class MailRead(ctk.CTkFrame):
    def __init__(self, parent, imap):
        super().__init__(parent, fg_color="#FFFFFF", corner_radius=0,height=700,width=550,border_width=2,border_color="#f0f0f0")

class MailWrite(ctk.CTkFrame):
    def __init__(self, parent, smtp, configs):
        super().__init__(parent, fg_color="#FFFFFF", corner_radius=0,height=700,width=550,border_width=2,border_color="#f0f0f0")