import re
import logging

from pymongo import MongoClient
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors.exceptions.bad_request_400 import AccessTokenExpired, AccessTokenInvalid

from info import API_ID, API_HASH, ADMINS
from info import DATABASE_URI as MONGO_URL



mongo_client = MongoClient(MONGO_URL)
mongo_db = mongo_client["cloned_bots"]

class clonedme(object):
    ME = None
    U_NAME = None
    B_NAME = None

@Client.on_message((filters.regex(r'\d[0-9]{8,10}:[0-9A-Za-z_-]{35}')) & filters.private)
async def on_clone(self, message):
    try:
        user_id = message.from_user.id
        user_name = message.from_user.first_name
        bot_token = re.findall(r'\d[0-9]{8,10}:[0-9A-Za-z_-]{35}', message.text, re.IGNORECASE)
        bot_token = bot_token[0] if bot_token else None
        bot_id = re.findall(r'\d[0-9]{8,10}', message.text)

        if not str(message.forward_from.id) != "93372553":
            msg = await message.reply_text(f" <code>{bot_token}</code>\n\n 🤍 𝑷𝒍𝒛 𝑾𝒂𝒊𝒕 𝑰 𝑻𝒓𝒚𝒊𝒏𝒈 𝑻𝒐 𝑪𝒍𝒐𝒏𝒆 𝒀𝒐𝒖𝒓 𝑩𝒐𝒕. 𝑾𝒂𝒊𝒕 𝑨 𝑴𝒊𝒏𝒖𝒕𝒆")
            try:
                ai = Client(
                    f"{bot_token}", API_ID, API_HASH,
                    bot_token=bot_token,
                    plugins={"root": "clone_plugins"},
                )
                await ai.start()
                bot = await ai.get_me()
                details = {
                    'bot_id': bot.id,
                    'is_bot': True,
                    'user_id': user_id,
                    'name': bot.first_name,
                    'token': bot_token,
                    'username': bot.username
                }
                mongo_db.bots.insert_one(details)
                clonedme.ME = bot.id
                clonedme.U_NAME = bot.username
                clonedme.B_NAME = bot.first_name
                await msg.edit_text(f"<u>𝘚𝘶𝘤𝘤𝘦𝘴𝘧𝘶𝘭𝘭𝘺 𝘊𝘭𝘰𝘯𝘦𝘥 𝘠𝘰𝘶𝘳 𝘉𝘰𝘵 </u> @{bot.username} .\n\n⚠️ <u>𝑫𝒐 𝑵𝒐𝒕 𝑺𝒆𝒏𝒅 𝑻𝒐 𝑨𝒏𝒚 𝑶𝒏𝒆 𝑻𝒉𝒆 𝑴𝒆𝒔𝒔𝒂𝒈𝒆 𝑾𝒊𝒕𝒉 <b>Bᴏᴛ Tᴏᴋᴇɴ</b></u> 𝐨𝐟 𝐲𝐨𝐮𝐫 𝐛𝐨𝐭, 𝑊ℎ𝑜 ℎ𝑎𝑠 𝑖𝑡 𝑐𝑎𝑛 𝑐𝑜𝑛𝑡𝑟𝑜𝑙 𝑦𝑜𝑢𝑟 𝐵𝑜𝑡!\n<i>𝑖𝑓 𝑦𝑜𝑢 𝑡ℎ𝑖𝑛𝑘 𝐴𝑛𝑦𝑜𝑛𝑒 𝑓𝑜𝑢𝑛𝑑 𝑜𝑢𝑡 𝑌𝑜𝑢𝑟 𝐵𝑜𝑡 𝑇𝑜𝑘𝑒𝑛, 𝐺𝑜 𝑇𝑜 @Botfather, 𝑈𝑠𝑒 /revoke 𝑎𝑛𝑑 𝑡ℎ𝑒𝑛 𝐹𝑜𝑟𝑤𝑎𝑟𝑑 𝑁𝑒𝑤 𝑇𝑜𝑘𝑒𝑛</i>")
            except BaseException as e:
                logging.exception("Error while cloning bot.")
                await msg.edit_text(f"⚠️ <b>𝑩𝑶𝑻 𝑬𝑹𝑹𝑶𝑹:</b>\n\n<code>{e}</code>\n\n❔ 𝑭𝒐𝒓𝒘𝒂𝒓𝒅 𝑻𝒉𝒊𝒔 𝑴𝒆𝒔𝒔𝒂𝒈𝒆 𝑻𝒐 @Aswanthcreater 𝑻𝒐 𝑩𝒆 𝑭𝒊𝒙𝒆𝒅.")
    except Exception as e:
        logging.exception("Error while handling message.")

async def get_bot():
    await ai.start()
    crazy = await ai.get_me()
    await ai.stop()
    return crazy


@Client.on_message(filters.command("clonedbots") & filters.private)
async def cloned_bots_list(client, message):
    try:
        user_id = message.from_user.id
        user_name = message.from_user.first_name

        bots = list(mongo_db.bots.find({'user_id': user_id}))

        if len(bots) == 0:
            await message.reply_text("You haven't cloned any bots yet.")
            return

        text = "<b>Your cloned bots:</b>\n\n"

        for bot in bots:
            text += f"- @{bot['username']} ({bot['name']})\n"
            text += f"  Bot ID: {bot['bot_id']}\n"
            text += f"  Token: {bot['token']}\n"
            text += "\n"

        await message.reply_text(text)
    except Exception as e:
        logging.exception("𝙴𝚛𝚛𝚘𝚛 𝚆𝚑𝚒𝚕𝚎 𝙷𝚊𝚗𝚍𝚕𝚒𝚗𝚐 𝙲𝚕𝚘𝚗𝚎𝚍 𝙱𝚘𝚝𝚜 𝙲𝚘𝚖𝚖𝚊𝚗𝚍.")

@Client.on_message(filters.command('cloned_count') & filters.private)
async def cloned_count(client, message):
    user_id = message.from_user.id
    if user_id not in ADMINS:
        await message.reply_text("𝚈𝚘𝚞 𝙰𝚛𝚎 𝙽𝚘𝚝 𝙰𝚞𝚝𝚑𝚘𝚛𝚒𝚣𝚎𝚍 𝚃𝚘 𝚄𝚜𝚎 𝚃𝚑𝚒𝚜 𝙲𝚘𝚖𝚖𝚊𝚗𝚍.")
        return
    cloned_bots = mongo_db.bots.find()
    count = cloned_bots.count()
    if count == 0:
        await message.reply_text("𝙽𝚘 𝙱𝚘𝚝𝚜 𝙷𝚊𝚟𝚎 𝙱𝚎𝚎𝚗 𝙲𝚕𝚘𝚗𝚎𝚍 𝚈𝚎𝚝.")
    else:
        bot_usernames = [f"@{bot['username']}" for bot in cloned_bots]
        bot_usernames_text = '\n'.join(bot_usernames)
        await message.reply_text(f"{count} bots have been cloned:\n\n{bot_usernames_text}")

@Client.on_message(filters.command(["removebot"]) & filters.user(ADMINS))
async def remove_bot(client: Client, message: Message):
    bot_username = message.text.split(" ", maxsplit=1)[1].strip()
    bot_data = mongo_db.bots.find_one_and_delete({"username": bot_username})

    if bot_data:
        bot_id = bot_data["bot_id"]
        cloned_sessions = mongo_db.cloned_sessions.find({"bot_id": bot_id})
        if cloned_sessions.count() > 0:
            for session in cloned_sessions:
                await session.stop()
                mongo_db.cloned_sessions.delete_one({"_id": session["_id"]})
        await message.reply_text(f"Bot @{bot_username} removed successfully.")
    else:
        await message.reply_text(f"Bot @{bot_username} is not in the cloned bots list.")

@Client.on_message(filters.command("deletecloned") & filters.private)
async def delete_cloned_bot(client, message):
    try:
        bot_token = re.findall(r'\d[0-9]{8,10}:[0-9A-Za-z_-]{35}', message.text, re.IGNORECASE)
        bot_token = bot_token[0] if bot_token else None
        bot_id = re.findall(r'\d[0-9]{8,10}', message.text)

        cloned_bot = mongo_collection.find_one({"token": bot_token})
        if cloned_bot:
            mongo_collection.delete_one({"token": bot_token})
            await message.reply_text("The cloned bot has been removed from the list and its details have been removed from the database.")
        else:
            await message.reply_text("The bot token provided is not in the cloned list.")
    except Exception as e:
        logging.exception("Error while deleting cloned bot.")
        await message.reply_text("An error occurred while deleting the cloned bot.")
