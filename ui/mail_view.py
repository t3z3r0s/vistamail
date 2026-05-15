import customtkinter as ctk
from customtkinter import CTkFrame, CTkButton, CTkLabel, CTkScrollableFrame

class MailView(ctk.CTkFrame):
    def __init__(self, parent, imap, smtp, configs):
        super().__init__(parent,fg_color="#FFFFFF",corner_radius=0)

        self._corner_radius=0
        self.imap = imap
        self.smtp = smtp
        self.configs = configs




class MailRead(ctk.CTkFrame):
    pass

class MailWrite(ctk.CTkFrame):
    pass