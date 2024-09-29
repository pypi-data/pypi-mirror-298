import os
from dotenv import load_dotenv

def Get_ENV(key):
    return os.getenv(key)

def Load_ENV():    
    load_dotenv()