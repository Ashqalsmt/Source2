import html
import os

from telethon.tl import functions
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName

from ..Config import Config
from . import ALIVE_NAME, BOTLOG, BOTLOG_CHATID, zq_lo, edit_delete
from ..sql_helper.globals import gvarstatus, addgvar, delgvar


plugin_category = "العروض"
DEFAULTUSER = gvarstatus("FIRST_NAME") or ALIVE_NAME
DEFAULTUSERBIO = Config.DEFAULT_BIO or "- ‏وحدي أضيء، وحدي أنطفئ انا قمري و كُل نجومي..🤍"
ANTHAL = gvarstatus("ANTHAL") or "(اعادة الحساب|اعادة|اعاده)"


async def get_full_user(event):
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.forward:
            replied_user = await event.client(
                GetFullUserRequest(
                    previous_message.forward.sender_id or previous_message.forward.channel_id
                )
            )
            return replied_user, None
        replied_user = await event.client(GetFullUserRequest(previous_message.sender_id))
        return replied_user, None
    else:
        input_str = event.pattern_match.group(1)
        if event.message.entities:
            ent = event.message.entities[0]
            if isinstance(ent, MessageEntityMentionName):
                user_id = ent.user_id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user, None
        try:
            user = await event.client.get_entity(input_str)
            replied_user = await event.client(GetFullUserRequest(user.id))
            return replied_user, None
        except Exception as e:
            return None, e


async def store_original_profile(event):
    me = await event.client(GetFullUserRequest("me"))
    if not gvarstatus("FIRST_NAME"):
        addgvar("FIRST_NAME", me.users[0].first_name or "")
    if not gvarstatus("LAST_NAME"):
        addgvar("LAST_NAME", me.users[0].last_name or "")
    if not gvarstatus("DEFAULT_BIO"):
        addgvar("DEFAULT_BIO", me.full_user.about or "")


@zq_lo.rep_cmd(pattern="(?:نسخ|انتحال)(?:\s|$)([\s\S]*)")
async def _(event):
    await store_original_profile(event)
    replied_user, error_i_a = await get_full_user(event)
    if replied_user is None:
        return await edit_delete(event, str(error_i_a))

    user_id = replied_user.users[0].id

    # تحميل الصورة إذا وجدت
    profile_pic = await event.client.download_profile_photo(user_id, Config.TEMP_DIR)
    if profile_pic is None:
        profile_pic = None

    # جلب الاسم والبايو
    first_name = html.escape(replied_user.users[0].first_name or "").replace("\u2060", "")
    last_name = replied_user.users[0].last_name
    last_name = html.escape(last_name or "").replace("\u2060", "") if last_name else "⁪⁬⁮⁮⁮⁮ ‌‌‌‌"
    user_bio = replied_user.full_user.about or ""

    # تحديث المعلومات
    await event.client(functions.account.UpdateProfileRequest(first_name=first_name))
    await event.client(functions.account.UpdateProfileRequest(last_name=last_name))
    await event.client(functions.account.UpdateProfileRequest(about=user_bio))

    # رفع الصورة
    if profile_pic:
        try:
            pfile = await event.client.upload_file(profile_pic)
            await event.client(functions.photos.UploadProfilePhotoRequest(pfile))
            os.remove(profile_pic)  # تنظيف الملف المؤقت
        except Exception as e:
            return await edit_delete(event, f"**اووبس خطـأ بالانتحـال:**\n__{e}__")

    await edit_delete(event, "**「❖╎تـم انتحـال الشخـص .. بنجـاح ༗**")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#الانتحـــال\n ⪼ تم انتحـال حسـاب الشخـص ↫ [{first_name}](tg://user?id={user_id}) بنجاح ✅",
        )


@zq_lo.rep_cmd(pattern=f"{ANTHAL}$")
async def revert(event):
    firstname = gvarstatus("FIRST_NAME") or DEFAULTUSER
    lastname = gvarstatus("LAST_NAME") or ""
    bio = gvarstatus("DEFAULT_BIO") or DEFAULTUSERBIO

    await event.client(
        functions.photos.DeletePhotosRequest(await event.client.get_profile_photos("me", limit=1))
    )
    await event.client(functions.account.UpdateProfileRequest(about=bio))
    await event.client(functions.account.UpdateProfileRequest(first_name=firstname))
    await event.client(functions.account.UpdateProfileRequest(last_name=lastname))

    await edit_delete(event, "**「❖╎تمت اعادة الحساب لوضعـه الاصلـي \n「❖╎والغـاء الانتحـال .. بنجـاح ✅**")

    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "#الغـاء_الانتحـال\n**⪼ تم الغـاء الانتحـال .. بنجـاح ✅**\n**⪼ تم إعـاده معلـوماتك الى وضعـها الاصـلي**",
        )
