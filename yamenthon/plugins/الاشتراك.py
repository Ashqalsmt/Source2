# yamenthon
import asyncio
import requests
import logging

from telethon import events, Button
from telethon.tl.functions.messages import ExportChatInviteRequest
from yamenthon import zq_lo, BOTLOG_CHATID
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from ..Config import Config
from ..core.managers import edit_delete, edit_or_reply
from ..core.logger import logging

LOGS = logging.getLogger(__name__)
plugin_category = "الادمن"


# تعيين قناة الاشتراك الاجباري للخاص
@zq_lo.rep_cmd(pattern="(ضع الاشتراك خاص|وضع الاشتراك خاص)(?:\s|$)([\s\S]*)")
async def set_private_channel(event):
    input_str = event.pattern_match.group(2)
    if input_str:
        try:
            p = await event.client.get_entity(input_str)
        except Exception as e:
            return await edit_delete(event, f"`{e}`", 5)
        try:
            channel_id = f"-100{p.id}"
            delgvar("Custom_Pm_Channel")
            addgvar("Custom_Pm_Channel", channel_id)
            return await edit_or_reply(
                event, f"**❖ تم تعيين قناة الاشتراك للخاص بنجاح\n\n• يوزر/اسم : `{input_str}`\n• ايدي : `{p.id}`\n\n• ارسل الآن `.اشتراك خاص`**"
            )
        except Exception as e:
            LOGS.error(str(e))
            return await edit_or_reply(event, "❖ خطأ في تعيين القناة")
    elif event.reply_to_msg_id:
        delgvar("Custom_Pm_Channel")
        addgvar("Custom_Pm_Channel", event.chat_id)
        return await edit_or_reply(event, f"**❖ تم تعيين قناة الاشتراك للخاص بنجاح\n\n• ايدي : `{event.chat_id}`\n• ارسل الآن `.اشتراك خاص`**")
    else:
        return await edit_or_reply(event, "❖ يرجى إدخال يوزر القناة أو الرد داخل القناة نفسها")


# تعيين قناة الاشتراك الاجباري للكروب
@zq_lo.rep_cmd(pattern="(ضع الاشتراك كروب|وضع الاشتراك كروب)(?:\s|$)([\s\S]*)")
async def set_group_channel(event):
    input_str = event.pattern_match.group(2)
    if input_str:
        try:
            p = await event.client.get_entity(input_str)
        except Exception as e:
            return await edit_delete(event, f"`{e}`", 5)
        try:
            channel_id = f"-100{p.id}"
            delgvar("Custom_G_Channel")
            addgvar("Custom_G_Channel", channel_id)
            return await edit_or_reply(
                event, f"**❖ تم تعيين قناة الاشتراك للكروب بنجاح\n\n• يوزر/اسم : `{input_str}`\n• ايدي : `{p.id}`\n\n• ارسل الآن `.اشتراك كروب`**"
            )
        except Exception as e:
            LOGS.error(str(e))
            return await edit_or_reply(event, "❖ خطأ في تعيين القناة")
    elif event.reply_to_msg_id:
        delgvar("Custom_G_Channel")
        addgvar("Custom_G_Channel", event.chat_id)
        return await edit_or_reply(event, f"**❖ تم تعيين قناة الاشتراك للكروب بنجاح\n\n• ايدي : `{event.chat_id}`\n• ارسل الآن `.اشتراك كروب`**")
    else:
        return await edit_or_reply(event, "❖ يرجى إدخال يوزر القناة أو الرد داخل القناة")


# تفعيل الاشتراك
@zq_lo.rep_cmd(pattern="اشتراك")
async def enable_subscription(event):
    ty = event.text.replace(".اشتراك", "").strip()
    group_types = ["كروب", "جروب", "قروب", "مجموعة", "مجموعه"]
    if ty in group_types:
        if not event.is_group:
            return await edit_delete(event, "❖ هذا الأمر يخص المجموعات فقط")
        if gvarstatus("sub_group") == event.chat_id:
            return await edit_delete(event, "❖ الاشتراك مفعّل بالفعل في هذه المجموعة")
        if gvarstatus("sub_group"):
            return await edit_or_reply(event, "❖ الاشتراك مفعل في مجموعة أخرى\n❖ أرسل `.تعطيل كروب` لإلغائه أولاً")
        addgvar("sub_group", event.chat_id)
        return await edit_or_reply(event, "✅ تم تفعيل الاشتراك الإجباري في هذه المجموعة")
    elif ty == "خاص":
        if gvarstatus("sub_private"):
            return await edit_delete(event, "❖ الاشتراك في الخاص مفعل مسبقًا")
        addgvar("sub_private", True)
        return await edit_or_reply(event, "✅ تم تفعيل الاشتراك الإجباري في الخاص")
    else:
        return await edit_delete(event, "❖ حدد نوع الاشتراك:\n`.اشتراك كروب`\n`.اشتراك خاص`")


# تعطيل الاشتراك
@zq_lo.rep_cmd(pattern="تعطيل")
async def disable_subscription(event):
    cc = event.text.replace(".تعطيل", "").strip()
    group_types = ["كروب", "جروب", "قروب", "مجموعة", "مجموعه", "الكروب", "اشتراك الكروب"]
    private_types = ["خاص", "الخاص", "اشتراك الخاص"]
    if cc in group_types:
        if not gvarstatus("sub_group"):
            return await edit_delete(event, "❖ الاشتراك في الكروب غير مفعّل")
        delgvar("sub_group")
        return await edit_delete(event, "✅ تم تعطيل الاشتراك الإجباري في الكروب")
    elif cc in private_types:
        if not gvarstatus("sub_private"):
            return await edit_delete(event, "❖ الاشتراك في الخاص غير مفعّل")
        delgvar("sub_private")
        return await edit_delete(event, "✅ تم تعطيل الاشتراك الإجباري في الخاص")
    else:
        return await edit_delete(event, "❖ حدد نوع الاشتراك لإلغائه:\n`.تعطيل كروب`\n`.تعطيل خاص`")


# التحقق من الاشتراك في الخاص
@zq_lo.rep_cmd(incoming=True, func=lambda e: e.is_private, edited=False, forword=None)
async def check_subscription_private(event):
    chat = await event.get_chat()
    admin_ids = (6669024587, 5571722913)
    user_id = (await event.get_sender()).id
    if user_id in admin_ids or chat.bot:
        return
    if gvarstatus("sub_private"):
        try:
            tok = Config.TG_BOT_TOKEN
            ch = gvarstatus("Custom_Pm_Channel")
            ch = int(ch)
            url = f"https://api.telegram.org/bot{tok}/getchatmember?chat_id={ch}&user_id={user_id}"
            reqt = requests.get(url).text

            if any(err in reqt for err in ["chat not found", "bot was kicked"]):
                mb = (await zq_lo.tgbot.get_me()).username
                await zq_lo.tgbot.send_message(
                    BOTLOG_CHATID,
                    f"❖ تأكد أن البوت @{mb} موجود ومشرف في قناة الاشتراك"
                )
                return

            if "left" in reqt or "not found" in reqt:
                try:
                    c = await zq_lo.get_entity(ch)
                    chn = c.username
                    if not chn:
                        chn = (await zq_lo.tgbot(ExportChatInviteRequest(ch))).link
                    btn_url = chn if chn.startswith("https://") else f"https://t.me/{chn}"
                    await event.reply(
                        f"❖ للتحدث معي، يرجى الاشتراك في القناة:\n{btn_url}",
                        buttons=[[Button.url("اضغط للاشتراك 🗳", btn_url)]]
                    )
                    return await event.message.delete()
                except Exception as er:
                    await zq_lo.tgbot.send_message(BOTLOG_CHATID, f"❖ خطأ في توليد رابط القناة:\n{er}")
        except Exception as er:
            await zq_lo.tgbot.send_message(BOTLOG_CHATID, f"❖ خطأ غير متوقع:\n{er}")
