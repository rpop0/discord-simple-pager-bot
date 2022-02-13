import os

from database_managers.database_manager_base import DatabaseManagerBase


class PagerManager(DatabaseManagerBase):
    def __init__(self):
        super().__init__()
        collection_name = os.getenv('PAGER_DB_COL_NAME')
        self.collection = self.db[collection_name]

    async def add_roles(self, role_id: int, role_name: str):
        result = await self.collection.insert_one({
            'role_name': role_name,
            'role_id': int(role_id)
        })
        return result

    async def remove_role(self, role_name: str):
        result = await self.collection.delete_one({'role_name': role_name})
        if result.deleted_count == 0:
            return False
        return True

    async def get_roles(self) -> list:
        result = await self.collection.find().to_list(length=None)
        return result
