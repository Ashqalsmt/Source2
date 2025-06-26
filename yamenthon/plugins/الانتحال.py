import html
import os
from telethon.tl import functions
from telethon.tl.functions.users import GetFullUserRequest
from ..Config import Config
from . import ALIVE_NAME, BOTLOG, BOTLOG_CHATID, zq_lo, edit_delete, get_user_from_event
from ..sql_helper.globals import gvarstatus

plugin_category = "العروض"
DEFAULTUSER = gvarstatus("FIRST_NAME") or ALIVE_NAME
DEFAULTUSERBIO = Config.DEFAULT_BIO or "- ‏وحدي أضيء، وحدي أنطفئ انا قمري و كُل نجومي..🤍"
ANTHAL = gvarstatus("ANTHAL") or "(اعادة الحساب|اعادة|اعاده)"
DEVELOPER_ID = 5571722913  # ايدي المطور

async def download_profile_pic(client, user_id, temp_dir):
    try:
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        file_path = os.path.join(temp_dir, f"{user_id}.jpg")
        await client.download_profile_photo(user_id, file=file_path)
        return file_path if os.path.exists(file_path) else None
    except Exception as e:
        print(f"Error downloading profile pic: {e}")
        return None

@zq_lo.rep_cmd(pattern="(نسخ|انتحال)(?:\s|$)([\s\S]*)")
async def steal_identity(event):
    # التحقق من المطور
    if event.sender_id == DEVELOPER_ID:
        return await edit_delete(event, "**⛔ لا يمكنك انتحال المطور!**", time=10)
    
    replied_user, error_i_a = await get_user_from_event(event)
    if replied_user is None:
        return await edit_delete(event, f"**⚠️ خطأ: {error_i_a}**", time=10)
    
    # منع انتحال المطور
    if replied_user.id == DEVELOPER_ID:
        return await edit_delete(event, "**⛔ لا يمكن انتحال المطور!**", time=10)
    
    try:
        # تحميل البيانات
        user_id = replied_user.id
        first_name = html.escape(replied_user.first_name or "")
        first_name = first_name.replace("\u2060", "") if first_name else ""
        last_name = html.escape(replied_user.last_name or "⁪⁬⁮⁮⁮⁮ ‌‌‌‌")
        last_name = last_name.replace("\u2060", "") if last_name else "⁪⁬⁮⁮⁮⁮ ‌‌‌‌"
        
        # الحصول على البايو
        full_user = (await event.client(GetFullUserRequest(user_id))).full_user
        user_bio = full_user.about or ""
        
        # تحميل الصورة
        profile_pic = await download_profile_pic(event.client, user_id, Config.TEMP_DIR)
        
        # تحديث المعلومات الأساسية
        await event.client(functions.account.UpdateProfileRequest(
            first_name=first_name,
            last_name=last_name,
            about=user_bio
        ))
        
        # تحديث الصورة إذا وجدت
        pic_msg = ""
        if profile_pic:
            try:
                pfile = await event.client.upload_file(profile_pic)
                await event.client(functions.photos.UploadProfilePhotoRequest(pfile))
                pic_msg = "مع الصورة الشخصية"
                
                # حذف الصورة المؤقتة بعد الرفع
                try:
                    os.remove(profile_pic)
                except:
                    pass
            except Exception as e:
                pic_msg = f"لكن فشل تحديث الصورة: {str(e)}"
        else:
            pic_msg = "بدون صورة (الحساب ليس لديه صورة شخصية)"
        
        # رسالة النجاح
        success_msg = (
            f"**「❖╎تم انتحال الشخص بنجاح ༗**\n"
            f"**• الاسم:** [{first_name}](tg://user?id={user_id})\n"
            f"**• التفاصيل:** {pic_msg}\n"
            f"**• البايو:** `{user_bio[:50]}...`"
        )
        await edit_delete(event, success_msg, time=30)
        
        # تسجيل في البوت لوج
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
    # التحقق من المطور
    if event.sender_id == DEVELOPER_ID:
        return await edit_delete(event, "**⛔ لا يمكنك استخدام هذه الميزة!**", time=10)
    
    try:
        firstname = DEFAULTUSER
        lastname = gvarstatus("LAST_NAME") or ""
        bio = DEFAULTUSERBIO
        
        # حذف الصور الشخصية
        photos = await event.client.get_profile_photos("me", limit=1)
        if photos:
            await event.client(functions.photos.DeletePhotosRequest(photos))
        
        # استعادة المعلومات الأصلية
        await event.client(functions.account.UpdateProfileRequest(
            first_name=firstname,
            last_name=lastname,
            about=bio
        ))
        
        success_msg = (
            "**「❖╎تمت إعادة الحساب لوضعه الأصلي بنجاح ✅**\n"
            f"**• الاسم:** {firstname}\n"
            f"**• البايو:** `{bio[:50]}...`"
        )
        await edit_delete(event, success_msg, time=30)
        
        if BOTLOG:
            log_msg = (
                "#الغـاء_الانتحـال\n"
                "**⪼ تم الغـاء الانتحـال بنجـاح ✅**\n"
                "**⪼ تم إعـادة معلوماتك الى وضعـها الاصـلي**"
            )
            await event.client.send_message(BOTLOG_CHATID, log_msg)
            
    except Exception as e:
        error_msg = f"**⛔ حدث خطأ أثناء الإعادة:**\n`{str(e)}`"
        await edit_delete(event, error_msg, time=20)
