from database_managers.database_manager_base import DatabaseManagerBase


class PagerManager(DatabaseManagerBase):
    def __init__(self):
        super().__init__()
        self.collection = self.db['roles']

    async def add_roles(self, ctx, role_id: int, leader_role_id: int, role_name: str, role_channel: str) -> None:
        emoji = [str(em) for em in ctx.guild.emojis if role_name in str(em)][0]
        result = await self.collection.insert_one({
            'role_name': role_name,
            'role_channel': role_channel,
            'role_emoji': emoji,
            'role_id': int(role_id),
            'leader_role_id': int(leader_role_id)
        })
        return result

    async def get_roles(self) -> list:
        result = await self.collection.find().to_list(length=None)
        return result
