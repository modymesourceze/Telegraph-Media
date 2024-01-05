from config import Config
from pyrogram import Client, filters
from pyrogram.types import Message
from telegraph import upload_file
from pyrogram.types import (
  InlineKeyboardMarkup,
  InlineKeyboardButton,
  CallbackQuery
)
import os
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.enums import ParseMode, ChatMemberStatus  
import os
import random
import sqlite3
import re
from requests import *

teletips = Client("MediaToTelegraphLink",
    api_id=Config.APP_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.TG_BOT_TOKEN)
''

@teletips.on_message(filters.command('start') & filters.private)
async def start(client, message):
    text = f"""
اهلا {message.from_user.mention},
🔮أنا هنا لإنشاء روابط التلجراف لملفات الوسائط الخاصة بك.

👨🏼‍💻ما عليك سوى إرسال ملف وسائط صالح مباشرة إلى هذه الدردشة.
♻️انواع الملفات الصالحه هي:- 'jpeg', 'jpg', 'png', 'mp4' and 'gif'.

🌐لأنشاء الروابط في المجموعات,اضفني لمجموعه خارقه اي عامه وارسل الامر <code>/tl</code> ردا علي ملف وسائط صالح.
🖥 | [🔱 𝐒𝐎𝐔𝐑𝐂𝐄 𝐙𝐄 🔱](https://t.me/Source_Ze)

☣️ | [⧛ 𓆩 𝑴𝒐𝒅𝒚 ➫ ⁽𝑆₎𝑻𝒆𝒂𝒎 ࿐ 𝑫 𝒆 𝒗 𝒊 𝒍 𓆪 ⧚](https://t.me/ELHYBA)
            """
    await teletips.send_message(message.chat.id, text, disable_web_page_preview=True)
    

@teletips.on_message(filters.media & filters.private)
async def get_link_private(client, message):
    try:
        text = await message.reply("🔮انتظر قليلا...")
        async def progress(current, total):
            await text.edit_text(f"📥 جاري التنزيل... {current * 100 / total:.1f}%")
        try:
            location = f"./media/private/"
            local_path = await message.download(location, progress=progress)
            await text.edit_text("📤 جاري الرفع الي التليجراف...")
            upload_path = upload_file(local_path) 
            await text.edit_text(f"🌐 | رابط التليجراف:\n\n<code>https://telegra.ph{upload_path[0]}</code>")     
            os.remove(local_path) 
        except Exception as e:
            await text.edit_text(f"❌ | فشل رفع الملف\n\n<i>Reason: {e}</i>")
            os.remove(local_path) 
            return                 
    except Exception:
        pass        

@teletips.on_message(filters.command('tl'))
async def get_link_group(client, message):
    try:
        text = await message.reply("🔮انتظر قليلا...")
        async def progress(current, total):
            await text.edit_text(f"📥 جاري التنزيل... {current * 100 / total:.1f}%")
        try:
            location = f"./media/group/"
            local_path = await message.reply_to_message.download(location, progress=progress)
            await text.edit_text("📤 جاري الرفع الي التليجراف...")
            upload_path = upload_file(local_path) 
            await text.edit_text(f"🌐 | رابط التليجراف:\n\n<code>https://telegra.ph{upload_path[0]}</code>")     
            os.remove(local_path) 
        except Exception as e:
            await text.edit_text(f"❌ | فشل رفع الملف\n\n<i>Reason: {e}</i>")
            os.remove(local_path) 
            return         
    except Exception:
        pass                                           

print("تم تنصيب البوت بنجاح")
teletips.run()
