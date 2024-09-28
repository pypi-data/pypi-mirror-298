from ..secrets.secrets_manager import get_secret
import pymongo

class MongoClient:
    def __init__(self, client_name: str):
        self.client_name = client_name
        self.mongo_client = self._get_mongo_client()

    def _get_mongo_client(self):
        secrets = get_secret(f"ripikutils/mongo_params/{self.client_name}")
        return pymongo.MongoClient(secrets['mongoURI'])

    def get_collection(self, database_name: str, collection_name: str):
        return self.mongo_client[database_name][collection_name]

def initialize_mongo(client_name: str):
    return MongoClient(client_name)