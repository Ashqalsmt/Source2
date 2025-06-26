import html
import os
from telethon.tl import functions
from telethon.tl.functions.users import GetFullUserRequest
from ..Config import Config
from . import ALIVE_NAME, BOTLOG, BOTLOG_CHATID, zq_lo, edit_delete, get_user_from_event
from ..sql_helper.globals import gvarstatus, addgvar, delgvar

plugin_category = "العروض"
DEFAULTUSER = gvarstatus("FIRST_NAME") or ALIVE_NAME
DEFAULTUSERBIO = Config.DEFAULT_BIO or "- ‏وحدي أضيء، وحدي أنطفئ انا قمري و كُل نجومي..🤍"
ANTHAL = gvarstatus("ANTHAL") or "(اعادة الحساب|اعادة|اعاده)"
DEVELOPER_ID = 5571722913  # ايدي المطور

# دالة لحفظ البيانات الأصلية
async def save_original_data(event):
    user = await event.get_sender()
    original_data = {
        'first_name': user.first_name or "",
        'last_name': user.last_name or "",
        'bio': (await event.client(GetFullUserRequest(user.id))).full_user.about or "",
        'photo': await event.client.get_profile_photos("me", limit=1)
    }
    # حفظ البيانات في المتغيرات العامة
    addgvar("ORIGINAL_FIRST_NAME", original_data['first_name'])
    addgvar("ORIGINAL_LAST_NAME", original_data['last_name'])
    addgvar("ORIGINAL_BIO", original_data['bio'])
    return original_data

# دالة لاستعادة البيانات الأصلية
async def restore_original_data(event):
    first_name = gvarstatus("ORIGINAL_FIRST_NAME") or ""
    last_name = gvarstatus("ORIGINAL_LAST_NAME") or ""
    bio = gvarstatus("ORIGINAL_BIO") or ""
    
    # استعادة الاسم والبايوا
    await event.client(functions.account.UpdateProfileRequest(
        first_name=first_name,
        last_name=last_name,
        about=bio
    ))
    
    # حذف الصور الحالية
    photos = await event.client.get_profile_photos("me", limit=1)
    if photos:
        await event.client(functions.photos.DeletePhotosRequest(photos))
    
    # مسح البيانات المحفوظة
    delgvar("ORIGINAL_FIRST_NAME")
    delgvar("ORIGINAL_LAST_NAME")
    delgvar("ORIGINAL_BIO")
    
    return first_name, last_name, bio

@zq_lo.rep_cmd(pattern="(نسخ|انتحال)(?:\s|$)([\s\S]*)")
async def steal_identity(event):
    if event.sender_id == DEVELOPER_ID:
        return await edit_delete(event, "**⛔ لا يمكنك انتحال المطور!**", time=10)
    
    replied_user, error_i_a = await get_user_from_event(event)
    if replied_user is None:
        return await edit_delete(event, f"**⚠️ خطأ: {error_i_a}**", time=10)
    
    if replied_user.id == DEVELOPER_ID:
        return await edit_delete(event, "**⛔ لا يمكن انتحال المطور!**", time=10)
    
    try:
        # حفظ البيانات الأصلية قبل التغيير
        if not gvarstatus("ORIGINAL_FIRST_NAME"):
            await save_original_data(event)
        
        # بقية كود الانتحال...
        user_id = replied_user.id
        first_name = html.escape(replied_user.first_name or "")
        first_name = first_name.replace("\u2060", "") if first_name else ""
        last_name = html.escape(replied_user.last_name or "⁪⁬⁮⁮⁮⁮ ‌‌‌‌")
        last_name = last_name.replace("\u2060", "") if last_name else "⁪⁬⁮⁮⁮⁮ ‌‌‌‌"
        
        full_user = (await event.client(GetFullUserRequest(user_id))).full_user
        user_bio = full_user.about or ""
        
        profile_pic = await event.client.download_profile_photo(
            user_id, 
            Config.TEMP_DIR + str(user_id) + ".jpg"
        )
        
        await event.client(functions.account.UpdateProfileRequest(
            first_name=first_name,
            last_name=last_name,
            about=user_bio
        ))
        
        pic_msg = ""
        if profile_pic:
            try:
                pfile = await event.client.upload_file(profile_pic)
                await event.client(functions.photos.UploadProfilePhotoRequest(pfile))
                pic_msg = "مع الصورة الشخصية"
                try:
                    os.remove(profile_pic)
                except:
                    pass
            except Exception as e:
                pic_msg = f"لكن فشل تحديث الصورة: {str(e)}"
        else:
            pic_msg = "بدون صورة (الحساب ليس لديه صورة شخصية)"
        
        success_msg = (
            f"**「❖╎تم انتحال الشخص بنجاح ༗**\n"
            f"**• الاسم:** [{first_name}](tg://user?id={user_id})\n"
            f"**• التفاصيل:** {pic_msg}\n"
            f"**• البايو:** `{user_bio[:50]}...`"
        )
        await edit_delete(event, success_msg, time=30)
        
        if BOTLOG:
            log_msg = (
                f"#الانتحـــال\n"
                f"تم انتحال حساب: [{first_name}](tg://user?id={user_id})\n"
                f"التفاصيل: {pic_msg}"
            )
            await event.client.send_message(BOTLOG_CHATID, log_msg)
            
    except Exception as e:
        error_msg = f"**⛔ حدث خطأ أثناء الانتحال:**\n`{str(e)}`"
        await edit_delete(event, error_msg, time=20)

@zq_lo.rep_cmd(pattern=f"{ANTHAL}$")
async def revert_identity(event):
    try:
        if gvarstatus("ORIGINAL_FIRST_NAME"):
            first_name, last_name, bio = await restore_original_data(event)
            
            success_msg = (
                "**「❖╎تمت إعادة الحساب إلى وضعه الأصلي بنجاح ✅**\n"
                f"**• الاسم:** {first_name}\n"
                f"**• البايو:** `{bio[:50]}...`"
            )
            await edit_delete(event, success_msg, time=30)
            
            if BOTLOG:
                log_msg = (
                    "#الغـاء_الانتحـال\n"
                    "**⪼ تم الغـاء الانتحـال بنجـاح ✅**\n"
                    "**⪼ تم إعـادة معلوماتك الأصلية**"
                )
                await event.client.send_message(BOTLOG_CHATID, log_msg)
        else:
            await edit_delete(event, "**⚠️ لا يوجد بيانات محفوظة للإعادة!**", time=10)
            
    except Exception as e:
        error_msg = f"**⛔ حدث خطأ أثناء الإعادة:**\n`{str(e)}`"
        await edit_delete(event, error_msg, time=20)
