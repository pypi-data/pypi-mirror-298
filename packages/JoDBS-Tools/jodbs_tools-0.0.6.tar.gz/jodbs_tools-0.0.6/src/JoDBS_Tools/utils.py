import os
from dotenv import load_dotenv

def Get_ENV(key):
    return os.environ[key]

def Load_ENV():    
    load_dotenv()