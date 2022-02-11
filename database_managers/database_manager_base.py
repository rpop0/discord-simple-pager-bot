import os

import certifi
from motor.motor_asyncio import AsyncIOMotorClient


class DatabaseManagerBase:
    def __init__(self):
        self.ca = certifi.where()
        database = os.getenv("DISPATCH_DB_NAME")
        self.client = AsyncIOMotorClient(os.getenv("DISPATCH_DB_CONN"), tlsCAFile=self.ca)
        self.db = self.client[database]

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def close(self):
        self.client.close()
