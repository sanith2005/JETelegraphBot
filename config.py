import os


class Config(object):
    TG_BOT_TOKEN = os.environ.get("1805440021:AAGmF5LHyAAjpMOnrBgsucJ8Rur9MvP0DO8", "")

    APP_ID = int(os.environ.get("1204352805", 12345))

    API_HASH = os.environ.get("1524641cf5093da47691888ecffd1f2c", "")
