import os


class Config(object):
    TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "1878189222:AAH4Mlz8LaGZ3IRDDba4-sSu2eWlcqUWAi4")

    APP_ID = int(os.environ.get("APP_ID", 12345))

    API_HASH = os.environ.get("API_HASH", "1524641cf5093da47691888ecffd1f2c")
