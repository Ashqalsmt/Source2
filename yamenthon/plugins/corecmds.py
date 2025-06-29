#yamenthon

import asyncio
import os
from datetime import datetime
from pathlib import Path

from ..Config import Config
from ..core import CMD_INFO, PLG_INFO
from ..utils import load_module, remove_plugin
from . import CMD_HELP, CMD_LIST, SUDO_LIST, zq_lo, edit_delete, edit_or_reply, reply_id

plugin_category = "الادوات"

DELETE_TIMEOUT = 5
thumb_image_path = os.path.join(Config.TMP_DOWNLOAD_DIRECTORY, "thumb_image.jpg")


def plug_checker(plugin):
    plug_path = f"./yamenthon/plugins/{plugin}.py"
    return plug_path


@zq_lo.rep_cmd(
    pattern="نصب$",
    command=("تنصيب", plugin_category),
    info={
        "header": "To install an external plugin.",
        "description": "Reply to any external plugin(supported by cat) to install it in your bot.",
        "usage": "{tr}install",
    },
)
async def install(event):
    "To install an external plugin."
    if event.reply_to_msg_id:
        try:
            downloaded_file_name = await event.client.download_media(
                await event.get_reply_message(),
                "yamenthon/plugins/",
            )
            if "(" not in downloaded_file_name:
                path1 = Path(downloaded_file_name)
                shortname = path1.stem
                load_module(shortname.replace(".py", ""))
                await edit_delete(
                    event,
                    f"**- تـم تنصـيب المـلف** `{os.path.basename(downloaded_file_name)}` **.. بـ نجـاح ☑️**",
                    10,
                )
            else:
                os.remove(downloaded_file_name)
                await edit_delete(
                    event, "**- خطـأ .. هذا المـلف منصـب بالفعـل مسبقـاً**", 10
                )
        except Exception as e:
            await edit_delete(event, f"**- خطـأ :**\n`{e}`", 10)
            os.remove(downloaded_file_name)
    await asyncio.sleep(DELETE_TIMEOUT)
    await event.delete()


@zq_lo.rep_cmd(
    pattern="حمل ([\s\S]*)",
    command=("حمل", plugin_category),
    info={
        "header": "To load a plugin again. if you have unloaded it",
        "description": "To load a plugin again which you unloaded by {tr}unload",
        "usage": "{tr}load <plugin name>",
        "examples": "{tr}load markdown",
    },
)
async def load(event):
    "To load a plugin again. if you have unloaded it"
    shortname = event.pattern_match.group(1)
    try:
        try:
            remove_plugin(shortname)
        except BaseException:
            pass
        load_module(shortname)
        await edit_delete(event, f"**- تـم تحميـل المـلف** {shortname} **.. بـ نجـاح ☑️**", 10)
    except Exception as e:
        await edit_or_reply(
            event,
            f"Could not load {shortname} because of the following error.\n{e}",
        )


@zq_lo.rep_cmd(
    pattern="ارسل ([\s\S]*)",
    command=("ارسل", plugin_category),
    info={
        "header": "To upload a plugin file to telegram chat",
        "usage": "{tr}send <plugin name>",
        "examples": "{tr}send markdown",
    },
)
async def send(event):
    "To uplaod a plugin file to telegram chat"
    reply_to_id = await reply_id(event)
    thumb = thumb_image_path if os.path.exists(thumb_image_path) else None
    input_str = event.pattern_match.group(1)
    the_plugin_file = plug_checker(input_str)
    if os.path.exists(the_plugin_file):
        caat = await event.client.send_file(
            event.chat_id,
            the_plugin_file,
            force_document=True,
            allow_cache=False,
            reply_to=reply_to_id,
            thumb=thumb,
            caption=f"**➥ اسم الاضـافـه:-** `{input_str}`",
        )
        await event.delete()
    else:
        await edit_or_reply(event, "404: File Not Found")


@zq_lo.rep_cmd(
    pattern="الغاء حمل ([\s\S]*)",
    command=("حمل", plugin_category),
    info={
        "header": "To unload a plugin temporarily.",
        "description": "You can load this unloaded plugin by restarting or using {tr}load cmd. Useful for cases like seting notes in rose bot({tr}unload markdown).",
        "usage": "{tr}unload <plugin name>",
        "examples": "{tr}unload markdown",
    },
)
async def unload(event):
    "To unload a plugin temporarily."
    shortname = event.pattern_match.group(1)
    try:
        remove_plugin(shortname)
        await edit_or_reply(event, f"Unloaded {shortname} successfully")
    except Exception as e:
        await edit_or_reply(event, f"Successfully unload {shortname}\n{e}")


@zq_lo.rep_cmd(
    pattern="الغاء نصب ([\s\S]*)",
    command=("الغاء تنصيب", plugin_category),
    info={
        "header": "To uninstall a plugin temporarily.",
        "description": "To stop functioning of that plugin and remove that plugin from bot.",
        "note": "To unload a plugin permanently from bot set NO_LOAD var in heroku with that plugin name, give space between plugin names if more than 1.",
        "usage": "{tr}uninstall <plugin name>",
        "examples": "{tr}uninstall markdown",
    },
)
async def unload(event):
    "To uninstall a plugin."
    shortname = event.pattern_match.group(1)
    path = Path(f"yamenthon/plugins/{shortname}.py")
    if not os.path.exists(path):
        return await edit_delete(
            event, f"**- عـذراً لا يـوجـد هنـاك مـلف بـ اسـم {shortname} لـ الغـاء تنصيبـه ؟!**"
        )
    os.remove(path)
    if shortname in CMD_LIST:
        CMD_LIST.pop(shortname)
    if shortname in SUDO_LIST:
        SUDO_LIST.pop(shortname)
    if shortname in CMD_HELP:
        CMD_HELP.pop(shortname)
    try:
        remove_plugin(shortname)
        await edit_or_reply(event, f"**- تـم الغـاء تنصيب المـلف** {shortname} **.. بـ نجـاح ☑️**")
    except Exception as e:
        await edit_or_reply(event, f"**- تـم الغـاء تنصيب المـلف** {shortname} **.. بـ نجـاح ☑️**\n{e}")

