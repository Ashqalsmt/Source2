import asyncio
import random
import os

from telethon.errors import (
    ChannelInvalidError,
    ChannelPrivateError,
    ChannelPublicGroupNaError,
)
from telethon.tl import functions
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.messages import GetFullChatRequest

from yamenthon import zq_lo
from yamenthon.core.logger import logging
from ..core.managers import edit_or_reply, edit_delete
from ..sql_helper.globals import gvarstatus

plugin_category = "الادوات"

REPADD = gvarstatus("R_ADD") or "ضيف"

# ⬇ تحميل قائمة اليوزرات المضافة سابقًا
def load_added_users():
    if not os.path.exists("added_users.txt"):
        return set()
    with open("added_users.txt", "r") as f:
        return set([line.strip() for line in f.readlines()])


# ⬇ حفظ يوزر جديد بعد الإضافة
def save_user(user_id):
    with open("added_users.txt", "a") as f:
        f.write(f"{user_id}\n")


async def get_chatinfo(event):
    chat = event.pattern_match.group(1)
    chat_info = None
    if chat:
        try:
            chat = int(chat)
        except ValueError:
            pass
    if not chat:
        if event.reply_to_msg_id:
            replied_msg = await event.get_reply_message()
            if replied_msg.fwd_from and replied_msg.fwd_from.channel_id is not None:
                chat = replied_msg.fwd_from.channel_id
        else:
            chat = event.chat_id
    try:
        chat_info = await event.client(GetFullChatRequest(chat))
    except:
        try:
            chat_info = await event.client(GetFullChannelRequest(chat))
        except ChannelInvalidError:
            await event.reply("**╮ عـذراً ..﮼ لم يتم العثور ؏ المجموعة او القناة 𓅫╰**")
            return None
        except ChannelPrivateError:
            await event.reply(
                "**╮  لا يمكنني استخدام الامر ﮼؏ المجموعات او القنوات الخاصة ...𓅫╰**"
            )
            return None
        except ChannelPublicGroupNaError:
            await event.reply("**╮ عـذراً ..﮼ لم يتم العثور ؏ المجموعة او القناة 𓅫╰**")
            return None
        except (TypeError, ValueError):
            await event.reply("**╮  رابط المجموعـه غير صحيح ..𓅫╰**")
            return None
    return chat_info


@zq_lo.rep_cmd(pattern=f"{REPADD} ?(.*)")
async def get_users(event):
    sender = await event.get_sender()
    me = await event.client.get_me()
    if not sender.id == me.id:
        eva = await event.reply("**╮  جـاري الاضـافه .. الࢪجـاء الانتظـار ...𓅫╰**")
    else:
        eva = await event.edit("**╮  جـاري الاضـافه .. الࢪجـاء الانتظـار ...𓅫╰**.")
    REPTHON = await get_chatinfo(event)
    chat = await event.get_chat()
    if event.is_private:
        return await eva.edit("**╮  لا استطـيع اضافـة الاعضـاء هـنا 𓅫╰**")
    
    s = 0
    f = 0
    error = "None"
    added_users = load_added_users()

    await eva.edit("**╮  حـالة الإضافـه :**\n\n**╮  جـاري جـمع معـلومات الاعضـاء ...⏳**")

    async for user in event.client.iter_participants(REPTHON.full_chat.id):
        if str(user.id) in added_users:
            continue  # تم إضافته سابقًا، تجاهله

        try:
            if error.startswith("Too"):
                return await eva.edit(
                    f"**حـالة الأضـافة انتـهت مـع الأخـطاء**\n- (**ربـما هـنالك ضغـط عـلى الأمࢪ حاول مجدداً لاحقـاً 🧸**) \n**الـخطأ** : \n`{error}`\n\n• اضـافة `{s}` \n• خـطأ بأضافـة `{f}`"
                )

            await event.client(
                functions.channels.InviteToChannelRequest(channel=chat, users=[user.id])
            )
            s += 1
            save_user(user.id)  # حفظ المستخدم بعد الإضافة
            await asyncio.sleep(random.randint(10, 30))  # تأخير عشوائي بين 10 - 30 ثانية
            await eva.edit(
                f"**╮ جـاري الإضـافـه...⧑**\n\n• تـم إضافـة `{s}` \n• خـطأ بإضافـة `{f}` \n\n**× آخـر خـطأ:** `{error}`"
            )

        except Exception as e:
            error = str(e)
            f += 1

    return await eva.edit(
        f"**⌔∮ تـمت الإضافـه بنجـاح ✅** \n\n• تـم إضافـة `{s}` \n• خـطأ بإضافـة `{f}`"
            )
