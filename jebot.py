import os
import logging
from pyrogram import Client, filters
from telegraph import upload_file
from config import Config
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from helpers.database.access_db import db
from helpers.database.database import Database
from helpers.forcesub import ForceSub
from helpers.broadcast import broadcast_handler
from helpers.database.add_user import AddUserToDatabase
from helpers.database.check_user_ban_status import handle_user_ban_status
from helpers.humanbytes import humanbytes

Jebot = Client(
   "Telegraph Uploader",
   api_id=Config.APP_ID,
   api_hash=Config.API_HASH,
   bot_token=Config.TG_BOT_TOKEN,
)

@Jebot.on_message(filters.command('start'))
async def start(bot, message):
    if message.from_user.id in info.BANNED_USERS:
        await message.reply_text("Sorry, You are banned to use me ☹️ Please Contact  Bot Owner 😊")
        return
    await AddUserToDatabase(bot, message)
    FSub = await ForceSub(bot, message)
    if FSub == 400:
        return
    """Start command handler"""
    if len(message.command) > 1 and message.command[1] == 'subscribe':
        await message.reply(INVITE_MSG.format(message.from_user.mention))
    else:
        buttons = [
            [
                InlineKeyboardButton('Updates Channel 🗣', url='https://t.me/new_ehi'),
                InlineKeyboardButton('Go Inline 🎭', switch_inline_query=''),
            ],
            [
                InlineKeyboardButton('Search Media 🔎', switch_inline_query_current_chat=''),
            ],
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply(START_MSG.format(message.from_user.mention), reply_markup=reply_markup)

@Jebot.on_message(filters.command("help"))
async def help(client, message):
    if message.chat.type == 'private':   
        await Jebot.send_message(
               chat_id=message.chat.id,
               text="""<b>Telegraph Bot Help!

Just send a photo or video less than 5mb file size, I'll upload it to telegraph.

~ @Infinity_BOTs</b>""",
        reply_markup=InlineKeyboardMarkup(
                                [[
                                        InlineKeyboardButton(
                                            "Back", callback_data="start"),
                                        InlineKeyboardButton(
                                            "About", callback_data="about"),
                                  ],[
                                        InlineKeyboardButton(
                                            "Source Code", url="https://github.com/ImJanindu/JETelegraphBot")
                                    ]]
                            ),        
            disable_web_page_preview=True,        
            parse_mode="html")

@Client.on_message(filters.private & filters.command("broadcast") & filters.user(info.BOT_OWNER) & filters.reply)
async def _broadcast(_, bot: Message):
    await broadcast_handler(bot)


@Client.on_message(filters.private & filters.command("stats") & filters.user(info.BOT_OWNER))
async def show_status_count(_, bot: Message):
    total, used, free = shutil.disk_usage(".")
    total = humanbytes(total)
    used = humanbytes(used)
    free = humanbytes(free)
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    total_users = await db.total_users_count()
    await bot.reply_text(
        text=f"**Total Disk Space:** {total} \n**Used Space:** {used}({disk_usage}%) \n**Free Space:** {free} \n**CPU Usage:** {cpu_usage}% \n**RAM Usage:** {ram_usage}%\n\n**Total Users in DB:** `{total_users}`\n\n@{info.BOT_USERNAME} 🤖",
        parse_mode="Markdown",
        quote=True
    )

    
@Client.on_message(filters.private & filters.command("banuser") & filters.user(info.BOT_OWNER))
async def ban(bot, message):
    
    if len(message.command) == 1:
        await message.reply_text(
            f"Use this command to ban any user from the bot 😊\n\nUsage:\n\n`/banuser user_id ban_duration ban_reason`\n\nEg: `/banuser 1234567 28 You misused me.`\n This will ban user with id `1234567` for `28` days for the reason `You misused me` 😊",
            quote=True
        )
        return

    try:
        user_id = int(message.command[1])
        ban_duration = int(message.command[2])
        ban_reason = ' '.join(message.command[3:])
        ban_log_text = f"Banning user {user_id} for {ban_duration} days for the reason {ban_reason}."
        try:
            await bot.send_message(
                user_id,
                f"You are banned to use this bot for **{ban_duration}** day(s) for the reason __{ban_reason}__ ☹️\n\n**Message from the Bot Admin**"
            )
            ban_log_text += '\n\nUser notified successfully 😊'
        except:
            traceback.print_exc()
            ban_log_text += f"\n\nUser notification failed ☹️\n\n`{traceback.format_exc()}`"

        await db.ban_user(user_id, ban_duration, ban_reason)
        print(ban_log_text)
        await message.reply_text(
            ban_log_text,
            quote=True
        )
    except:
        traceback.print_exc()
        await message.reply_text(
            f"Error occoured ❗️ Traceback given below\n\n`{traceback.format_exc()}`",
            quote=True
        )


@Client.on_message(filters.private & filters.command("unbanuser") & filters.user(info.BOT_OWNER))
async def unban(bot, message):

    if len(message.command) == 1:
        await message.reply_text(
            f"Use this command to unban any user 😊\n\nUsage:\n\n`/unbanuser user_id`\n\nEg: `/unbanuser 1234567`\n This will unban user with id `1234567`.",
            quote=True
        )
        return

    try:
        user_id = int(message.command[1])
        unban_log_text = f"Unbanning user {user_id}"
        try:
            await bot.send_message(
                user_id,
                f"Your ban was lifted 😊"
            )
            unban_log_text += '\n\nUser notified successfully 😊'
        except:
            traceback.print_exc()
            unban_log_text += f"\n\nUser notification failed ☹️\n\n`{traceback.format_exc()}`"
        await db.remove_ban(user_id)
        print(unban_log_text)
        await message.reply_text(
            unban_log_text,
            quote=True
        )
    except:
        traceback.print_exc()
        await message.reply_text(
            f"Error occoured ❗️ Traceback given below\n\n`{traceback.format_exc()}`",
            quote=True
        )


@Client.on_message(filters.private & filters.command("bannedusers") & filters.user(info.BOT_OWNER))
async def _banned_usrs(_, bot: Message):
    
    all_banned_users = await db.get_all_banned_users()
    banned_usr_count = 0
    text = ''

    async for banned_user in all_banned_users:
        user_id = banned_user['id']
        ban_duration = banned_user['ban_status']['ban_duration']
        banned_on = banned_user['ban_status']['banned_on']
        ban_reason = banned_user['ban_status']['ban_reason']
        banned_usr_count += 1
        text += f"> **user_id**: `{user_id}`, **Ban Duration**: `{ban_duration}`, **Banned on**: `{banned_on}`, **Reason**: `{ban_reason}`\n\n"
    reply_text = f"Total banned user(s) of Leo Media Search Bot: `{banned_usr_count}`\n\n{text}"
    if len(reply_text) > 4096:
        with open('banned-users.txt', 'w') as f:
            f.write(reply_text)
        await bot.reply_document('banned-users.txt', True)
        os.remove('banned-users.txt')
        return
    await bot.reply_text(reply_text, True)
      
@Jebot.on_message(filters.command("about"))
async def about(client, message):
    if message.chat.type == 'private':   
        await Jebot.send_message(
               chat_id=message.chat.id,
               text="""<b>About Telegraph Bot!</b>

<b>♞ Developer:</b> <a href="https://t.me/ImJanindu">Janindu 🇱🇰</a>

<b>♞ Support:</b> <a href="https://t.me/InfinityBOTs_Support">Infinity BOTs Support</a>

<b>♞ Library:</b> <a href="https://github.com/pyrogram/pyrogram">Pyrogram</a>

<b>~ @Infinity_BOTs</b>""",
     reply_markup=InlineKeyboardMarkup(
                                [[
                                        InlineKeyboardButton(
                                            "Back", callback_data="help"),
                                        InlineKeyboardButton(
                                            "Source Code", url="https://github.com/ImJanindu/JETelegraphBot")
                                    ]]
                            ),        
            disable_web_page_preview=True,        
            parse_mode="html")

@Jebot.on_message(filters.photo)
async def telegraphphoto(client, message):
    msg = await message.reply_text("Uploading To Telegraph...")
    download_location = await client.download_media(
        message=message, file_name='root/jetg')
    try:
        response = upload_file(download_location)
    except:
        await msg.edit_text("Photo size should be less than 5mb!") 
    else:
        await msg.edit_text(f'**Uploaded To Telegraph!\n\n👉 https://telegra.ph{response[0]}\n\n~ @Infinity_BOTs**',
            disable_web_page_preview=True,
        )
    finally:
        os.remove(download_location)

@Jebot.on_message(filters.video)
async def telegraphvid(client, message):
    msg = await message.reply_text("Uploading To Telegraph...")
    download_location = await client.download_media(
        message=message, file_name='root/jetg')
    try:
        response = upload_file(download_location)
    except:
        await msg.edit_text("Video size should be less than 5mb!") 
    else:
        await msg.edit_text(f'**Uploaded To Telegraph!\n\n👉 https://telegra.ph{response[0]}\n\n~ @Infinity_BOTs**',
            disable_web_page_preview=True,
        )
    finally:
        os.remove(download_location)

@Jebot.on_message(filters.animation)
async def telegraphgif(client, message):
    msg = await message.reply_text("Uploading To Telegraph...")
    download_location = await client.download_media(
        message=message, file_name='root/jetg')
    try:
        response = upload_file(download_location)
    except:
        await msg.edit_text("Gif size should be less than 5mb!") 
    else:
        await msg.edit_text(f'**Uploaded To Telegraph!\n\n👉 https://telegra.ph{response[0]}\n\n~ @Infinity_BOTs**',
            disable_web_page_preview=True,
        )
    finally:
        os.remove(download_location)

@Jebot.on_callback_query()
async def button(bot, update):
      cb_data = update.data
      if "help" in cb_data:
        await update.message.delete()
        await help(bot, update.message)
      elif "about" in cb_data:
        await update.message.delete()
        await about(bot, update.message)
      elif "start" in cb_data:
        await update.message.delete()
        await start(bot, update.message)

print(
    """
Bot Started!
Join @Infinity_BOTs
"""
)

Jebot.run()
