from imap_tools import MailBox, AND


class Imap:
    def __init__(self, host=None, user=None, password=None, port=993):
        self.host     = host
        self.user     = user
        self.password = password
        self.port     = port

    def configure(self, host, user, password, port=993):
        self.host     = host
        self.user     = user
        self.password = password
        self.port     = port

    def fetch_headers(self, folder="INBOX", limit=100):
        with MailBox(self.host).login(self.user, self.password, initial_folder=folder) as mailbox:
            headers = []
            for msg in mailbox.fetch(AND(all=True), limit=limit, reverse=True, mark_seen=False, headers_only=True):
                headers.append({
                    "uid":     msg.uid,
                    "sender":  msg.from_,
                    "subject": msg.subject or "(no subject)",
                    "time":    msg.date,
                })
            return headers

    def fetch_body(self, uid, folder="INBOX"):
        with MailBox(self.host).login(self.user, self.password, initial_folder=folder) as mailbox:
            msgs = list(mailbox.fetch(AND(uid=uid), mark_seen=True))
            if msgs:
                return msgs[0].text or "(no content)"
        return ""

    def fetch_folders(self):
        with MailBox(self.host).login(self.user, self.password) as mailbox:
            return [folder.name for folder in mailbox.folder.list()]