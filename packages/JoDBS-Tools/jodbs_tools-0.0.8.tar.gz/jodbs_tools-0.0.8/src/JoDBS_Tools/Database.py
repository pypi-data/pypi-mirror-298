import requests
from pymongo import MongoClient, errors
from .utils import Get_ENV

class Database:
    def __init__(self, connection_string=None, collection=None):
        self.connection_string = connection_string or Get_ENV("CONNECTION_STRING")
        self.collection = collection
        self.client = None
        self.db = None

    def connect(self):
        try:
            self.client = MongoClient(self.connection_string)
            self.db = self.client[self.collection]
            print("MongoDB Connection: Successful ✔️")
        except errors.ServerSelectionTimeoutError as err:
            print(f"MongoDB Connection: Failed ❌ - {err}")
            raise Exception("MongoDB Connection: Failed ❌")

    def get_database(self):
        if not self.db:
            self.connect()
        return self.db
    
class BotNetworkConnection:
    def __init__(self, api_url=None, token=None):
        self.api_url = api_url or Get_ENV("API_URL")
        self.token = token or Get_ENV("API_TOKEN")
        self.headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }

    def get_data(self, endpoint):
        url = f"{self.api_url}/{endpoint}"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            print("API Connection: Successful ✔️", self.api_url, endpoint, response.status_code)
            return response.json()
        except requests.exceptions.HTTPError as err:
            print(f"API Connection: Failed ❌ - {err}")
            raise Exception("API Connection: Failed ❌")
        

    # Get Startup Data from API