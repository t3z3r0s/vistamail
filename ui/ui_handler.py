import sys
import os
import tkinter

import customtkinter as ctk
from PIL import Image
from PIL import ImageTk
from customtkinter import CTkLabel, CTkButton, CTkFrame, CTkEntry, CTkScrollableFrame, CTkCanvas

from ui.mail_view import MailView
from ui.settings_handler import SettingsFrame


class AuthWindow(ctk.CTkToplevel):
    def __init__(self, parent, account_manager, config_manager, cache_manager):
        super().__init__(parent)

        self.mainUI          = parent
        self.accounts        = account_manager
        self.configs         = config_manager
        self.cache           = cache_manager
        self.selected_email  = None
        self.account_rows    = []

        self.title("Login")
        self.geometry("1000x600")
        self.resizable(False, False)
        self.transient(parent)
        self.lift()
        self.focus_force()
        self.grab_set()
        self.overrideredirect(True)
        self.geometry_center(1000, 600)
        self.after(100, self._force_focus)

        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        img_path = os.path.join(self.script_dir, "../assets/icons/log-in_bg.jpg")
        self.vista_auth_bg = ctk.CTkImage(light_image=Image.open(img_path), size=(1000, 600))
        self.bg_image = CTkLabel(self, image=self.vista_auth_bg, text="")
        self.bg_image.place(x=0, y=0, anchor="nw")

        self.title_lbl = CTkLabel(
            self, text="vistamail", fg_color="#FFFEEE", text_color="black",
            bg_color="#FFFEEE", font=("Segoe UI Light", 30),
        )
        self.rights_lbl = CTkLabel(
            self, text="vistamail© 2026. All rights reserved.",
            text_color="#A9A9A9", fg_color="#FFFEEE",
            font=("Segoe UI Light", 13, "bold"),
        )
        self.close_btn = CTkLabel(
            self, text="x", font=("Segoe UI Light", 18, "bold"),
            fg_color="#33764A", width=20, height=20,
            text_color="#FFFFFF", bg_color="#33764A",
        )

        self.title_lbl.place(x=20,  y=10,  anchor="nw")
        self.rights_lbl.place(x=10, y=570, anchor="nw")
        self.close_btn.place(x=990, y=5,   anchor="ne")
        self.close_btn.bind("<Button-1>", self.close_login)

        self.title_lbl.tkraise()
        self.rights_lbl.tkraise()
        self.init_addacc()



    class AccountRow:
        COLOR_DEFAULT  = "#FFFEEE"
        COLOR_SELECTED = "#D3D3D3"

        def __init__(self, parent_widget, outer, email, data, pfp_image):
            self.outer = outer
            self.email = email
            self.data  = data

            self.frame = CTkFrame(parent_widget, height=50,
                                  fg_color=self.COLOR_DEFAULT, border_width=1)
            self.name_lbl  = CTkLabel(self.frame, font=("Segoe UI Light", 18),
                                       text=data.get("name", ""))
            self.email_lbl = CTkLabel(self.frame, font=("Segoe UI Light", 16, "italic"),
                                       text=email)
            self.pfp_lbl   = ctk.CTkLabel(self.frame, image=pfp_image, text="")

            self._bind_events()
            self._layout()

        def _layout(self):
            self.frame.pack(fill="x", pady=1)
            self.name_lbl.place(x=65,  y=1,  anchor="nw")
            self.email_lbl.place(x=65, y=21, anchor="nw")
            self.pfp_lbl.place(x=26,   y=25, anchor="c")
            self.name_lbl.lift()

        def _bind_events(self):
            for w in (self.frame, self.pfp_lbl, self.name_lbl, self.email_lbl):
                w.bind("<ButtonPress-1>",   self.on_press)
                w.bind("<ButtonRelease-1>", self.on_release)

        def on_press(self, event=None):
            self.frame.configure(fg_color=self.COLOR_SELECTED)

        def on_release(self, event=None):
            for row in self.outer.account_rows:
                row.frame.configure(fg_color=self.COLOR_DEFAULT)
            self.frame.configure(fg_color=self.COLOR_SELECTED)
            self.outer.selected_email = self.email
            self.outer.show_password_entry()



    def geometry_center(self, width, height):
        self.update_idletasks()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x  = (sw // 2) - (width  // 2)
        y  = (sh // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")


    def init_addacc(self):
        self.add_account_frame = CTkFrame(self, fg_color="#FFFEEE",
                                          width=400, height=600)
        self.add_account_frame.place(x=0, y=0, anchor="nw")

        for w in (self.title_lbl, self.rights_lbl, self.close_btn):
            w.tkraise()

        CTkLabel(
            self.add_account_frame, text="Welcome", fg_color="#FFFEEE",
            text_color="black", bg_color="#FFFEEE",
            font=("Segoe UI Light", 40),
        ).place(x=45, y=100, anchor="nw")

        self.add_name_entry = CTkEntry(
            self.add_account_frame, border_width=1, height=30, width=300,
            font=("Segoe UI", 17, "italic"), fg_color="#FFFEEE",
            border_color="#A9A9A9", placeholder_text="Name (optional)",
            placeholder_text_color="#A9A9A9", corner_radius=5,
        )
        self.add_name_entry.place(x=45, y=200, anchor="nw")

        self.add_email_entry = CTkEntry(
            self.add_account_frame, border_width=1, height=30, width=300,
            font=("Segoe UI", 17, "italic"), fg_color="#FFFEEE",
            border_color="#A9A9A9", placeholder_text="example555@hotmail.com",
            placeholder_text_color="#A9A9A9", corner_radius=5,
        )
        self.add_email_entry.place(x=45, y=250, anchor="nw")

        self.add_password_entry = CTkEntry(
            self.add_account_frame, border_width=1, height=30, width=300,
            font=("Segoe UI", 17, "italic"), fg_color="#FFFEEE",
            border_color="#A9A9A9", placeholder_text="Password",
            placeholder_text_color="#A9A9A9", show="*", corner_radius=5,
        )
        self.add_password_entry.place(x=45, y=300, anchor="nw")

        CTkButton(
            self.add_account_frame, text="Add account", fg_color="#33764b",
            font=("Segoe UI", 20), text_color="#FFFEEE", width=300,
            hover_color="#3c6b47", command=self.send_add_account_data,
        ).place(x=45, y=390, anchor="nw")

        CTkLabel(
            self.add_account_frame, text_color="#A9A9A9",
            text="Already have an account?", font=("Segoe UI", 15),
        ).place(x=45, y=440, anchor="nw")

        sign_in_lbl = CTkLabel(
            self.add_account_frame, text_color="#0078D7",
            text="Sign in", font=("Segoe UI", 15),
        )
        sign_in_lbl.place(x=230, y=440, anchor="nw")
        sign_in_lbl.bind("<Button-1>", lambda e: self._switch_to_login())

    def send_add_account_data(self):
        name     = self.add_name_entry.get().strip()
        email    = self.add_email_entry.get().strip()
        password = self.add_password_entry.get().strip()
        if self.accounts.append_account(name, email, password):
            self.add_account_frame.place_forget()
            self.init_login()


    def init_login(self):
        if hasattr(self, "signin_frame") and self.signin_frame.winfo_exists():
            self.signin_frame.destroy()

        self.signin_frame = CTkFrame(self, fg_color="#FFFEEE",
                                     width=400, height=600)
        self.signin_frame.place(x=0, y=0, anchor="nw")

        for w in (self.title_lbl, self.rights_lbl, self.close_btn):
            w.tkraise()

        CTkLabel(
            self.signin_frame, text="Sign in", fg_color="#FFFEEE",
            text_color="black", bg_color="#FFFEEE",
            font=("Segoe UI Light", 40),
        ).place(x=45, y=80, anchor="nw")

        self.accounts_holder = CTkScrollableFrame(
            self.signin_frame, bg_color="#FFFEEE", fg_color="#FFFEEE",
            width=300, height=150,
            scrollbar_button_color="#FFFEEE",
            scrollbar_button_hover_color="#FFFEEE",
        )
        self.no_accounts_lbl = CTkLabel(
            self.signin_frame,
            text="You have no accounts saved",
            fg_color="#FFFEEE", text_color="#A9A9A9",
            bg_color="#FFFEEE", font=("Segoe UI Light", 20),
        )

        all_accounts = self.accounts.load_all_accounts().get("accounts", {})
        self.account_rows = []

        pfp_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "../assets/icons/profile_pictures/default_user_pfp.jpg",
        )
        pfp_image = ctk.CTkImage(light_image=Image.open(pfp_path), size=(50, 48))

        if all_accounts:
            self.accounts_holder.place(x=40, y=160, anchor="nw")
            self.no_accounts_lbl.place_forget()
            for email, data in all_accounts.items():
                row = self.AccountRow(self.accounts_holder, self, email, data, pfp_image)
                self.account_rows.append(row)
        else:
            self.accounts_holder.place_forget()
            self.no_accounts_lbl.place(x=45, y=150, anchor="nw")

        self.login_password_entry = CTkEntry(
            self.signin_frame, border_width=1, height=30, width=300,
            font=("Segoe UI", 17, "italic"), fg_color="#FFFEEE",
            border_color="#A9A9A9", placeholder_text="Password",
            placeholder_text_color="#A9A9A9", show="*", corner_radius=5,
        )

        self.remember_var = ctk.BooleanVar(value=False)
        self.rememberme   = ctk.CTkCheckBox(
            self.signin_frame, text="Remember me",
            font=("Segoe UI", 15), fg_color="#33764b",
            hover_color="#327847", checkmark_color="#FFFEEE",
            border_width=1, corner_radius=3, variable=self.remember_var,
        )
        self.signin_button = CTkButton(
            self.signin_frame, text="Sign in", fg_color="#33764b",
            font=("Segoe UI", 20), text_color="#FFFEEE", width=300,
            hover_color="#3c6b47", command=self.send_login_data,
        )

        CTkLabel(
            self.signin_frame, text_color="#A9A9A9",
            text="Add an account:", font=("Segoe UI", 15),
        ).place(x=45, y=530, anchor="nw")

        add_link = CTkLabel(
            self.signin_frame, text_color="#0078D7",
            text="Add account", font=("Segoe UI", 15),
        )
        add_link.place(x=170, y=530, anchor="nw")
        add_link.bind("<Button-1>", lambda e: self._switch_to_add_account())

    def show_password_entry(self):
        self.login_password_entry.place(x=45, y=350, anchor="nw")
        self.rememberme.place(x=45, y=400)
        self.signin_button.place(x=45, y=460, anchor="nw")
        self.login_password_entry.focus_set()

    def send_login_data(self):
        if not self.selected_email:
            print("No account selected.")
            return

        email    = self.selected_email
        password = self.login_password_entry.get().strip()
        remember = self.remember_var.get()

        success, account_data, config_data = self.accounts.verify_account_credentials(email, password)

        if success:
            self.accounts.update_configs(email, rememberme=remember)
            self.cache.append_cache_data(email)

            if remember:
                self.accounts.store_plain_password(email, password)
            else:
                self.accounts.delete_plain_password(email)

            self.on_login_success(email, account_data)
        else:
            print("Credentials are invalid.")



    def on_login_success(self, email, account_data):
        domain_data = account_data[email]["domain_data"]
        password    = self.accounts.get_plain_password(email)

        self.mainUI.imap.configure(
            host=domain_data["imap"]["server"],
            user=email,
            password=password,
            port=domain_data["imap"]["port"],
        )
        self.mainUI.smtp.configure(
            host=domain_data["smtp"]["server"],
            user=email,
            password=password,
        )

        self.destroy()
        self.mainUI.deiconify()
        self.mainUI.load_mainUI()


    def _force_focus(self):
        try:
            self.focus_force()
            self.grab_set()
        except tkinter.TclError:
            pass

    def _switch_to_login(self):
        self.add_account_frame.place_forget()
        self.init_login()

    def _switch_to_add_account(self):
        if hasattr(self, "signin_frame") and self.signin_frame.winfo_exists():
            self.signin_frame.place_forget()
        self.add_account_frame.place(x=0, y=0, anchor="nw")

    def close_login(self, event=None):
        if self.winfo_exists():
            sys.exit()


class vistamailUI(ctk.CTk):
    def __init__(self, imap, smtp, accountManager, configManager, cacheManager):
        super().__init__()
        self.imap       = imap
        self.smtp       = smtp
        self.accountMngr = accountManager
        self.configMngr  = configManager
        self.cacheMngr   = cacheManager
        self.script_dir  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.toplogo_path   = os.path.join(self.script_dir, "assets", "icons", "vistamail_logos", "Vistamail(32).png")
        self.wallpaper_path = os.path.join(self.script_dir, "assets", "icons", "log-in_bg.jpg")

        self.after(0, self.login_query)

    def login_query(self):
        if self.cacheMngr.logged_in_query():
            email = self.cacheMngr.load_cache_data()

            if email:
                password = self.accountMngr.get_plain_password(email)

                if not password:
                    # plain password missing — force re-login
                    self.withdraw()
                    self.auth_window = AuthWindow(self, self.accountMngr, self.configMngr, self.cacheMngr)
                    return

                account_data = self.accountMngr.load_account_data(email)
                domain_data = account_data[email]["domain_data"]

                self.imap.configure(
                    host=domain_data["imap"]["server"],
                    user=email,
                    password=password,
                    port=domain_data["imap"]["port"],
                )
                self.smtp.configure(
                    host=domain_data["smtp"]["server"],
                    user=email,
                    password=password,
                )

            self.load_mainUI()
        else:
            self.withdraw()
            self.auth_window = AuthWindow(self, self.accountMngr, self.configMngr, self.cacheMngr)



    def load_mainUI(self):
        self.title("vistamail")
        self.deiconify()
        self.overrideredirect(True)
        self.geometry("1200x800")

        self.sidebarcanvas = CTkCanvas(self, width=1200, height=800, highlightthickness=0)
        self.sidebarcanvas.place(x=0, y=0)

        img = Image.open(self.wallpaper_path)
        img = img.resize((1200, 800), Image.Resampling.LANCZOS)
        self.wallpaper_img = ImageTk.PhotoImage(img)
        self.sidebarcanvas.create_image(0, 0, image=self.wallpaper_img, anchor="nw")

        self.mainUIholder = CTkFrame(self, width=1000, height=800, fg_color="#FFFFFF", corner_radius=0)
        self.mainUIholder.place(x=200, y=0)

        self.mail_view = MailView(self.mainUIholder, self.imap, self.smtp, self.configMngr, self.cacheMngr)
        self.mail_view.place(x=30, y=70, anchor="nw")

        self.settings_view = SettingsFrame(self, self.configMngr, self.accountMngr)

        self.settingsButton = ctk.CTkButton(
            self, command=self.settings_view.open_self, text="Settings",
            font=("Segoe UI Light", 16), width=160, height=30,
            fg_color="#FFFFFF", text_color="#222222", hover_color="#A9A9A9", corner_radius=0,
        )
        self.settingsButton.place(x=20, y=750, anchor="nw")

        self.search_inbox = CTkEntry(
            self.mainUIholder, placeholder_text="Search emails:",
            border_color="#f0f0f0", height=30, width=230,
            fg_color="#FFFFFF", font=("Segoe UI", 16),
        )
        self.search_inbox.place(x=30, y=60, anchor="sw")

        self.filter_search = ctk.CTkComboBox(
            self.mainUIholder, values=["New -> Old", "Old -> New", "By Size"],
            height=30, width=110, dropdown_font=("Segoe UI", 12),
            dropdown_fg_color="#FFFFFF", fg_color="#FFFFFF",
            border_color="#f0f0f0", button_color="#f0f0f0",
        )
        self.filter_search.place(x=270, y=60, anchor="sw")

        self.refresh_emails = CTkButton(
            self.mainUIholder, width=30, height=30, text="⟳",
            fg_color="#FFFFFF", border_color="#FFFFFF",
            text_color="#111111", hover_color="#f2f2f2",
            font=("Segoe UI", 18), command=self.mail_view.load_emails,
        )
        self.refresh_emails.place(x=390, y=60, anchor="sw")

        self.closebutton = CTkLabel(
            self, text_color="#111111", text="x",
            font=("Segoe UI", 22, "bold"), fg_color="#FFFFFF",
        )
        self.closebutton.place(x=1180, y=10, anchor="ne")
        self.closebutton.bind("<Button-1>", self.close_mainUI)

        self._drag_x = 0
        self._drag_y = 0
        self.bind("<ButtonPress-1>", self.drag_window)
        self.bind("<B1-Motion>",     self.drag_window)

        def widget_ui_hover_enter(event):
            canvas = event.widget
            item   = canvas.find_withtag("current")[0]
            canvas.itemconfig(item, fill="#A9A9A9")

        def widget_ui_hover_leave(event):
            canvas = event.widget
            item   = canvas.find_withtag("current")[0]
            canvas.itemconfig(item, fill="white")

        self.vistatitle       = self.sidebarcanvas.create_text(100, 50,  text="vistamail", fill="white", font=("Segoe UI Light", 30))
        self.inboxspacer      = self.sidebarcanvas.create_line(25, 100, 175, 100, fill="#CACACA", width=1)
        self.primarybtn       = self.sidebarcanvas.create_text(57,  130, text="Primary",   fill="white", font=("Segoe UI Light", 13))
        self.favoritesbtn     = self.sidebarcanvas.create_text(63,  160, text="Favorited", fill="white", font=("Segoe UI Light", 13))
        self.sentbtn          = self.sidebarcanvas.create_text(45,  190, text="Sent",      fill="white", font=("Segoe UI Light", 13))
        self.secondaryspacer  = self.sidebarcanvas.create_line(25, 220, 175, 220, fill="#CACACA", width=1)
        self.draftsbtn        = self.sidebarcanvas.create_text(51,  240, text="Drafts",    fill="white", font=("Segoe UI Light", 13))
        self.junkbtn          = self.sidebarcanvas.create_text(46,  270, text="Junk",      fill="white", font=("Segoe UI Light", 13))
        self.spambtn          = self.sidebarcanvas.create_text(50,  300, text="Spam",      fill="white", font=("Segoe UI Light", 13))

        self.inboxfolderwidgets = [
            self.primarybtn, self.junkbtn, self.favoritesbtn,
            self.sentbtn, self.draftsbtn, self.spambtn,
        ]
        for widget in self.inboxfolderwidgets:
            self.sidebarcanvas.tag_bind(widget, "<Enter>", widget_ui_hover_enter)
            self.sidebarcanvas.tag_bind(widget, "<Leave>", widget_ui_hover_leave)



    def drag_window(self, event):
        if event.type == "4" and event.y < 30:
            self._drag_x = event.x_root - self.winfo_x()
            self._drag_y = event.y_root - self.winfo_y()
        elif event.type == "6" and event.y < 30:
            x = event.x_root - self._drag_x
            y = event.y_root - self._drag_y
            self.geometry(f"+{x}+{y}")

    def close_mainUI(self, event=None):
        sys.exit()