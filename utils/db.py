# utils/db.py

import certifi
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from config import Config


class Database:
    def __init__(self):
        self.client = None
        self.db = None

    def connect(self):
        if not Config.MONGODB_URI:
            raise Exception("MONGODB_URI not found in .env file")

        try:
            if self.client is None:
                self.client = MongoClient(
                    Config.MONGODB_URI,
                    tls=True,
                    tlsCAFile=certifi.where(),
                    serverSelectionTimeoutMS=5000
                )

                # Test connection
                self.client.admin.command("ping")

                # Select database
                self.db = self.client[Config.DATABASE_NAME]

                print("MongoDB Connected Successfully")
                print("Connected Database:", self.db.name)

        except ConnectionFailure as e:
            print("MongoDB Connection Failed:", str(e))
            raise

    def get_collection(self, name):
        if self.db is None:
            raise Exception("Database not connected. Call connect() first.")
        return self.db[name]


# Create singleton instance (without connecting yet)
database = Database()
