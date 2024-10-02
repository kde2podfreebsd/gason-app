import aiosqlite
import os


class DatabaseSingleton:
    _instance = None

    def __new__(cls, db_path="database.db"):
        if cls._instance is None:
            cls._instance = super(DatabaseSingleton, cls).__new__(cls)
            cls.db_path = db_path
        return cls._instance

    async def _load_sql(self, filename):
        with open(filename, 'r') as file:
            return file.read()

    async def init_db(self):
        if not os.path.exists(self.db_path):
            async with aiosqlite.connect(self.db_path) as db:
                user_table_sql = await self._load_sql("database/sql/users_table.sql")
                admin_table_sql = await self._load_sql("database/sql/admins_table.sql")
                event_table_sql = await self._load_sql("database/sql/events_table.sql")
                event_file_table_sql = await self._load_sql("database/sql/event_files_table.sql")

                await db.execute(user_table_sql)
                await db.execute(admin_table_sql)
                await db.execute(event_table_sql)
                await db.execute(event_file_table_sql)
                await db.commit()

    async def get_db(self):
        return await aiosqlite.connect(self.db_path)


db_instance = DatabaseSingleton()
