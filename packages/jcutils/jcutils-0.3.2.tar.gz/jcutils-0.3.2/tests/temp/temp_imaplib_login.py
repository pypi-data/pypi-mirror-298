import imaplib

# def login():
#     M = imaplib.IMAP4_SSL(config.email.server, ssl_context=None)
#     M.login(config.email.address, config.email.password)
#     M.select("INBOX", readonly=False)
#     return M


def login():
    M = imaplib.IMAP4_SSL("imap.189.cn", ssl_context=None)
    M.login("19901718151@189.cn", "qhU8ssvcER")
    M.select("INBOX", readonly=False)
    return M


m = login()
print(m.state)
