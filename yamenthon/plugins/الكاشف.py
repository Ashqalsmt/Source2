#𝙔𝘼𝙈𝙀𝙉𝙏𝙃𝙊𝙉 ®
#الملـف حقـوق وكتابـة زلـزال الهيبـه ⤶ @T_A_Tl خاص بسـورس ⤶ 𝙔𝘼𝙈𝙀𝙉𝙏𝙃𝙊𝙉
#الملف مرفـوع ع استضـافتـي مهمـا خمطت راح تطلـع حقـــوقــي بســورســـك
#هههههههههههههههههه


import asyncio
import os

from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError

from yamenthon import zq_lo

from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import reply_id
from . import BOTLOG, BOTLOG_CHATID

plugin_category = "البحث"


BaqirPH_cmd = (
    "𓆩 [𝗦𝗼𝘂𝗿𝗰𝗲 𝙔𝘼𝙈𝙀𝙉𝙏𝙃𝙊𝙉 𝗖𝗼𝗻𝗳𝗶𝗴 📲 - كـاشـف الارقـام العربيــة](t.me/YamenThon) 𓆪\n\n"
    "**⪼ الامــر ↵**\n\n"
    "⪼ `.كاشف` + اسـم الدولـة + الـرقـم بـدون مفتـاح الـدولة\n\n"
    "**⪼ الوصـف :**\n"
    "**- لجـلب معلـومـات عـن رقـم هـاتف معيـن**\n\n"
    "**⪼ مثـال :**\n\n"
    "`.كاشف اليمن 777887798` \n\n"
    "`.كاشف السعوديه 555542317` \n\n"
    "`.كاشف الامارات 43171234` \n\n"
    "**الامـر يدعـم الـدول التـاليـة ↵** 🇾🇪🇸🇦🇦🇪🇰🇼🇶🇦🇧🇭🇴🇲 \n\n"
    "🛃 سيتـم اضـافة المزيـد من الدول قريبـاً\n\n"
    "\n𓆩 [𐇮 ✗ ¦ ↱𓄂𝑨𝑺𝑯𝑬𝑸 𝑨𝑳𝑺𝑨𝑴𝑻↲ ¦ ✗  𐇮](t.me/T_A_Tl) 𓆪"
)


@zq_lo.rep_cmd(
    pattern="كاشف ?(.*)",
    command=("كاشف", plugin_category),
    info={
        "header": "لـ جـلب معلـومـات عـن رقـم هـاتف معيـن .. الامـر يدعـم الـدول التـاليـة ↵ 🇾🇪🇸🇦🇦🇪🇰🇼🇶🇦🇧🇭🇴🇲 .. سيـتم اضـافـة بقيـة الـدول العـربيـة قريبـاً",
        "الاستـخـدام": "{tr}كاشف + اسـم الدولـة + الـرقـم بـدون مفتـاح الـدولة",
    },
)
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    reply_to_id = await reply_id(event)
    if event.reply_to_msg_id and not event.pattern_match.group(1):
        reply_to_id = await event.get_reply_message()
        reply_to_id = str(reply_to_id.message)
    else:
        reply_to_id = str(event.pattern_match.group(1))
    if not reply_to_id:
        return await edit_or_reply(
            event, "**╮ . كـاشف الاࢪقـام الـ؏ـࢪبيـة 📲.. اࢪسـل** `.الكاشف` **للتعليـمات 𓅫╰**"
        )
    chat = "@Zelzalybot"
    zzzzl1l = await edit_or_reply(event, "**╮•⎚ جـارِ الكـشف ؏ــن الـرقـم  📲 ⌭ . . .**")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=1194140165)
            )
            await event.client.send_message(chat, "{}".format(input_str))
            response = await response
            await event.client.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await zzzzl1l.edit("**╮•⎚ تحـقق من انـك لم تقـم بحظر البوت @Zelzalybot .. ثم اعـد استخدام الامـر ...🤖♥️**")
            return
        if response.text.startswith("I can't find that"):
            await zzzzl1l.edit("**╮•⎚ عـذراً .. لـم استطـع ايجـاد المطلـوب ☹️💔**")
        else:
            await zzzzl1l.delete()
            await event.client.send_message(event.chat_id, response.message)



# Copyright (C) 2022 Zed-Thon . All Rights Reserved
@zq_lo.rep_cmd(pattern="الكاشف")
async def cmd(baqir):
    await edit_or_reply(baqir, BaqirPH_cmd)

