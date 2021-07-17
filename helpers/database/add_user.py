import info
from helpers.database.access_db import db
from pyrogram import Client
from pyrogram.types import Message


async def AddUserToDatabase(bot: Client, cmd: Message):
    if not await db.is_user_exist(cmd.from_user.id):
        await db.add_user(cmd.from_user.id)
        if info.-1001457779051 is not None:
            await bot.send_message(
                int(info.-1001457779051),
                f"#NEW_USER: \n\nNew User [{cmd.from_user.first_name}](tg://user?id={cmd.from_user.id}) started @{(await bot.get_me()).username} 😊"
            )
