from models import User, Admin, Event

class DBHandler:
    def __init__(self, db_instance):
        self.db_instance = db_instance

    async def add_user(self, user: User):
        async with await self.db_instance.get_db() as db:
            await db.execute(
                "INSERT INTO users (chatid, username, first_name, second_name, phone, qrcode_path) VALUES (?, ?, ?, ?, ?, ?)",
                (user.chatid, user.username, user.first_name, user.second_name, user.phone, user.qrcode_path),
            )
            await db.commit()

    async def add_admin(self, admin: Admin):
        async with await self.db_instance.get_db() as db:
            await db.execute(
                "INSERT INTO admins (chatid, username, qr_code_background, qr_code_type) VALUES (?, ?, ?, ?)",
                (admin.chatid, admin.username, admin.qr_code_background, admin.qr_code_type.value),
            )
            await db.commit()

    async def add_event(self, event: Event):
        async with await self.db_instance.get_db() as db:
            async with db.execute(
                "INSERT INTO events (text, inst_post_url, tg_post_url, button_text, admin_chatid) VALUES (?, ?, ?, ?, ?)",
                (event.text, event.inst_post_url, event.tg_post_url, event.button_text, event.admin_chatid)
            ) as cursor:
                event_id = cursor.lastrowid

            if len(event.files) > 10:
                raise Exception("Превышено максимальное количество файлов для одного события (10).")

            for file_path in event.files:
                await db.execute(
                    "INSERT INTO event_files (event_id, file_path) VALUES (?, ?)",
                    (event_id, file_path),
                )
            await db.commit()

    async def get_event_files(self, event_id: int):
        async with await self.db_instance.get_db() as db:
            async with db.execute(
                "SELECT file_path FROM event_files WHERE event_id = ?", (event_id,)
            ) as cursor:
                return [row[0] for row in await cursor.fetchall()]
