import os

from config import load_config

config = load_config()

if config.get("to_translate", []) != []:
    def get_feps():
        return config.get("to_translate")
else:
    def get_feps(): 
        return os.listdir("./fep/fep")