import customtkinter as ctk
from customtkinter import CTkFrame, CTkButton, CTkLabel, CTkScrollableFrame


class MailView(ctk.CTkFrame):
    def __init__(self, parent, imap, smtp, configs, cache):
        super().__init__(parent, fg_color="#FFFFFF", corner_radius=0, height=700, width=400, border_width=2, border_color="#f0f0f0")
        self.imap = imap
        self.smtp = smtp
        self.configs = configs
        self.cache = cache
        self.email_rows = []

        self.mr = MailRead(parent, self.imap)
        self.mr.place(x=420, y=70, anchor="nw")
        self.mw = MailWrite(parent, self.smtp, self.configs)

        self.mainScrollingFrame = CTkScrollableFrame(
            self, fg_color="#FFFFFF", corner_radius=2,
            border_color="#F0F0F0", border_width=2,
            scrollbar_fg_color="#FFFFFF", scrollbar_button_color="#FFFFFF",
            scrollbar_button_hover_color="#FFFFFF"
        )
        self.mainScrollingFrame.place(x=0, y=0, relwidth=1.0, relheight=1.0)

        self.load_emails()

    def load_emails(self):
        for row in self.email_rows:
            row.MailRowFrame.destroy()
        self.email_rows = []

        headers = self.imap.fetch_headers()
        for header in headers:
            row = MailHeaders(
                self.mainScrollingFrame, self,
                header["uid"],
                header["sender"],
                header["subject"],
                header["time"],
            )
            self.email_rows.append(row)



class MailHeaders:
    def __init__(self, parent, mail_view, uid, sender, subject, time):
        self.mail_view = mail_view
        self.uid       = uid

        self.MailRowFrame = CTkFrame(
            parent, height=70, fg_color=self.COLOR_DEFAULT,
            border_color="#E0E0E0", border_width=2
        )
        self.MailRowFrame.pack(fill="x", pady=1)



class MailRead(ctk.CTkFrame):
    def __init__(self, parent, imap):
        super().__init__(parent, fg_color="#FFFFFF", corner_radius=0, height=700, width=550, border_width=2, border_color="#f0f0f0")
        self.imap = imap

        self.no_selected_lbl = CTkLabel(
            self, text="No email selected.",
            font=("Segoe UI Light", 18), text_color="#A9A9A9"
        )
        self.no_selected_lbl.place(x=275, y=350, anchor="c")




class MailWrite(ctk.CTkFrame):
    def __init__(self, parent, smtp, configs):
        super().__init__(parent, fg_color="#FFFFFF", corner_radius=0, height=700, width=550, border_width=2, border_color="#f0f0f0")
        self.smtp    = smtp
        self.configs = configs