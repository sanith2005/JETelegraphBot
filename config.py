import os


class Config(object):
    TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "")

    APP_ID = int(os.environ.get("APP_ID", 12345))

    API_HASH = os.environ.get("API_HASH", "")
    
    MONGODB_URI = os.environ.get("MONGODB_URI", "mongodb+srv://Erichdaniken:Erichdaniken@cluster0.tf4rj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    
    DATABASE_NAME = environ['DATABASE_NAME',]
    
    MONGODB_URI = os.environ.get("MONGODB_URI", "mongodb+srv://Erichdaniken:Erichdaniken@cluster0.tf4rj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    
    LOG_CHANNEL = int(os.environ.get("-1001431641448", -1001431641448))
 
    SESSION = environ.get('SESSION', '1BVtsOIsBu0BihEEghJO6JHCUFCtx4-X-gg71s2uwxNvDZRMFJ3n2gT2U-AbEkMCcmF6uk3t3ZU5o3HvKEQwZRdKtVyS3rLRk8pU4SYJIvDp1PCeDZx8DgEQ1ctEbG0cVhtLpNaNyTiXW2jDXHwNVj8QlLbNkN6fCtlyTpIZdsR8btC513Nu_l2hAYkwx2pwDtLJZSUOsvnxkZyIxRQrsoYVthn_FS7MPHEmXnzI5P6LJZdJ2QC-vUJM5-A5rSxznG3EkhtGYjG3NoSIIs8y1XFWzRTD_Pvw8wkVrvFRicMZN_BRp9iGCkd1IG46VZghA8zA_yf4zfzfToldMuQXOEXIrc-ksxx0=')
    
    BANNED_CHAT_IDS = list(set(int(x) for x in os.environ.get("BANNED_CHAT_IDS", "-1001362659779 -1001255795497").split()))
    
    BANNED_USERS = set(int(x) for x in os.environ.get("BANNED_USERS", "1234567890").split())
    
    UPDATES_CHANNEL = os.environ.get("-1001431641448", None)
    
    BROADCAST_AS_COPY = bool(os.environ.get("BROADCAST_AS_COPY", ""))
    
    SESSION_NAME = os.environ.get("SESSION_NAME", "LeoMediaSearchBot")

    START_MSG = "test"
