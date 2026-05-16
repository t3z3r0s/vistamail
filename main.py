from core.SMTP import Smtp
from core.IMAP import Imap
from core.accounts import AccountManager
from core.accounts import ConfigManager
from core.accounts import CacheManager
from ui.ui_handler import vistamailUI


def main():
    accountManager = AccountManager()
    configManager = ConfigManager()
    cacheManager = CacheManager()

    # inject dependencies AFTER creation
    accountManager.set_dependencies(configManager, cacheManager)
    configManager.set_account_dependencies(accountManager)
    cacheManager.set_account_dependencies(accountManager)

    imap = Imap()
    smtp = Smtp()

    vista = vistamailUI(imap, smtp, accountManager, configManager, cacheManager)

    try:
        vista.mainloop()
    except KeyboardInterrupt:
        print("vistamail stopped manually.")


if __name__ == '__main__':
    main()