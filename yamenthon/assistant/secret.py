import json
import os
import re

from telethon.events import CallbackQuery
from telethon.tl.functions.users import GetUsersRequest

from yamenthon import zq_lo
from ..sql_helper.globals import gvarstatus


@zq_lo.tgbot.on(CallbackQuery(data=re.compile(b"secret_(.*)")))
async def on_plug_in_callback_query_handler(event):
    timestamp = int(event.pattern_match.group(1).decode("UTF-8"))
    uzerid = gvarstatus("hmsa_id")
    ussr = int(uzerid) if uzerid.isdigit() else uzerid
    try:
        rrr = await zq_lo.get_entity(ussr)
    except ValueError:
        rrr = await zq_lo(GetUsersRequest(ussr))
    if os.path.exists("./yamenthon/secret.txt"):
        jsondata = json.load(open("./yamenthon/secret.txt"))
        try:
            message = jsondata[f"{timestamp}"]
            userid = message["userid"]
            ids = [userid, zq_lo.uid, rrr.id]
            if event.query.user_id in ids:
                encrypted_tcxt = message["text"]
                reply_pop_up_alert = encrypted_tcxt
            else:
                reply_pop_up_alert = "مطـي الهمسـه مـو الك 🦓"
        except KeyError:
            reply_pop_up_alert = "- عـذراً .. هذه الرسـالة لم تعد موجـوده في البوت"
    else:
        reply_pop_up_alert = "- عـذراً .. هذه الرسـالة لم تعد موجـوده في البـوت"
    await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
