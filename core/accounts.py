import json
import re
import keyring
import os
from json import JSONDecodeError

## about 70% of this file is hand written by me, ai did help me on this, however i can recite what every line does in detail


class AccountManager:
    def __init__(self):
        self.configs = None
        self.cache = None
        self.accounts = {}
        self.current_account = None

        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.account_json_dir = os.path.join(self.script_dir, "..", "data", "user_accounts.json")
        self.config_json_dir  = os.path.join(self.script_dir, "..", "data", "user_settings.json")

        self.PROVIDERS = {
            "gmail.com":   {"imap": {"server": "imap.gmail.com",          "port": 993},
                            "smtp": {"server": "smtp.gmail.com",           "port_ssl": 465, "port_tls": 587}},
            "yahoo.com":   {"imap": {"server": "imap.mail.yahoo.com",     "port": 993},
                            "smtp": {"server": "smtp.mail.yahoo.com",      "port_ssl": 465, "port_tls": 587}},
            "outlook.com": {"imap": {"server": "outlook.office365.com",   "port": 993},
                            "smtp": {"server": "smtp.office365.com",       "port_ssl": 465, "port_tls": 587}},
            "hotmail.com": {"imap": {"server": "outlook.office365.com",   "port": 993},
                            "smtp": {"server": "smtp.office365.com",       "port_ssl": 465, "port_tls": 587}},
            "icloud.com":  {"imap": {"server": "imap.mail.me.com",        "port": 993},
                            "smtp": {"server": "smtp.mail.me.com",         "port_ssl": 465, "port_tls": 587}},
        }

        self.DEFAULT_CONFIG = {
            "rememberme":    False,
            "darkmode":      False,
            "notifications": False,
        }

    def set_dependencies(self, config_mngr, cache_mngr):
        self.configs = config_mngr
        self.cache   = cache_mngr

    def domain_suffix_data(self, email):
        if "@" not in email:
            raise ValueError("Invalid email")
        domain = email.split("@")[1]
        return self.PROVIDERS.get(domain)

    def is_valid_email(self, email):
        if not isinstance(email, str):
            return False
        regex = r"^[^@\s\.]+(\.[^@\s\.]+)*@[^@\s\.]+(\.[^@\s\.]+)+$"
        return re.match(regex, email) is not None

    def is_valid_password(self, password):
        return isinstance(password, str) and len(password) >= 8

    def append_account(self, name, email, password):
        if not self.is_valid_email(email):
            raise ValueError("Invalid email")
        if not self.is_valid_password(password):
            raise ValueError("Invalid password")

        data = _read_json(self.account_json_dir, {"accounts": {}})
        self.accounts = data.get("accounts", {})

        if email in self.accounts:
            raise ValueError("Account already exists")

        self.default_pfp_path = os.path.join(
            self.script_dir,
            "../assets/icons/profile_pictures/default_user_pfp.jpg",
        )

        self.accounts[email] = {"name": name or None,
                                "pfp": self.default_pfp_path,
                                "server_data":self.domain_suffix_data(email)}
        data["accounts"] = self.accounts

        _write_json(self.account_json_dir, data)
        keyring.set_password("vistamail", email, password)
        return True

    def load_config_data(self, email):
        if not self.configs:
            raise RuntimeError("ConfigManager not injected")
        return self.configs.load_config_data(email)



    def verify_account_credentials(self, email, password):
        stored = keyring.get_password("vistamail", email)
        if stored != password:
            return False, None, None
        return True, self.load_account_data(email), self.load_config_data(email)


    def load_account_data(self, email):
        data     = _read_json(self.account_json_dir, {"accounts": {}})
        accounts = data.get("accounts", {})

        if email not in accounts:
            raise ValueError("Account not found")

        acc = accounts[email]
        return {
            email: {
                "name":        acc["name"],
                "pfp":         acc["pfp"],
                "domain_data": self.domain_suffix_data(email),
            }
        }

    def load_all_accounts(self):
        return _read_json(self.account_json_dir, {"accounts": {}})

    def update_configs(self, email, **kwargs):
        if not self.configs:
            raise RuntimeError("ConfigManager not injected")
        self.configs.update_configs(email, **kwargs)



def _read_json(path, default):
    if not os.path.exists(path):
        _write_json(path, default)
        return default

    with open(path, "r", encoding="utf-8") as f:
        content = f.read().strip()

    if not content:
        _write_json(path, default)
        return default

    try:
        return json.loads(content)
    except JSONDecodeError:
        _write_json(path, default)
        return default


def _write_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


class ConfigManager:
    def __init__(self):
        self.account_manager = None
        self.config_json_dir = None
        self.DEFAULT_CONFIG  = None

    def set_account_dependencies(self, account_manager):
        self.account_manager = account_manager
        self.config_json_dir = account_manager.config_json_dir
        self.DEFAULT_CONFIG  = account_manager.DEFAULT_CONFIG

    def load_config_data(self, email, **kwargs):
        data    = _read_json(self.config_json_dir, {"configs": {}})
        configs = data.setdefault("configs", {})

        configs.setdefault(email, self.DEFAULT_CONFIG.copy())

        for k, v in kwargs.items():
            configs[email][k] = v

        data["configs"] = configs
        _write_json(self.config_json_dir, data)

        return {email: configs[email]}

    def update_configs(self, email, **kwargs):
        data    = _read_json(self.config_json_dir, {"configs": {}})
        configs = data.setdefault("configs", {})
        configs.setdefault(email, self.DEFAULT_CONFIG.copy())

        for k, v in kwargs.items():
            configs[email][k] = v

        _write_json(self.config_json_dir, data)


class CacheManager:
    def __init__(self):
        self.accountManager = None

        self.script_dir       = os.path.dirname(os.path.abspath(__file__))
        self.cache_json_dir   = os.path.join(self.script_dir, "..", "data", "user_cache.json")
        self.config_json_dir  = os.path.join(self.script_dir, "..", "data", "user_settings.json")

    def set_account_dependencies(self, account_manager):
        self.accountManager = account_manager

    def append_cache_data(self, email):
        _write_json(self.cache_json_dir, {"logged_in": email})

    def load_cache_data(self):
        try:
            logged_in_email =  _read_json(self.cache_json_dir, {}).get("logged_in", {})
            logged_in_password = keyring.get_password("vistamail", logged_in_email)
            if logged_in_email and logged_in_password:
                return logged_in_email, logged_in_password
            return None, None
        except Exception:
            return None, None

    def logged_in_query(self):
        email, password = self.load_cache_data()
        remember_me_checked = _read_json(self.config_json_dir, {}).get("configs",{}).get(email, {}).get("rememberme",False)
        #print(f"user logged into current session: {email}, {password}")
        if email and password and remember_me_checked:
            return True
        return False