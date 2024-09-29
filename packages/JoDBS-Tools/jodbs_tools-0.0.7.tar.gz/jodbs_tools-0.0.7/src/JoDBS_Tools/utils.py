import os
from dotenv import load_dotenv

def Load_ENV():
    load_dotenv()

def Get_ENV(key):
    try:
        return os.environ[key]
    except KeyError:
        raise KeyError(f"Environment variable '{key}' not found.")