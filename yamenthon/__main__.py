import sys, asyncio
import yamenthon
from yamenthon import BOTLOG_CHATID, HEROKU_APP, PM_LOGGER_GROUP_ID
from telethon import functions
from .Config import Config
from .core.logger import logging
from .core.session import zq_lo
from .utils import mybot, saves, autoname
from .utils import add_bot_to_logger_group, load_plugins, setup_bot, startupmessage, verifyLoggerGroup
from .sql_helper.globals import addgvar, delgvar, gvarstatus

LOGS = logging.getLogger("YAMENTHON")
cmdhr = Config.COMMAND_HAND_LER

if gvarstatus("ALIVE_NAME") is None: #Code by T.me/T_A_Tl
    try:
        LOGS.info("⌭ بـدء إضافة الاسـم التلقـائـي ⌭")
        zq_lo.loop.run_until_complete(autoname())
        LOGS.info("✓ تـم إضافة فار الاسـم .. بـنجـاح ✓")
    except Exception as e:
        LOGS.error(f"- The AutoName {e}")

try:
    LOGS.info("⌭ بـدء تنزيـل يـــمنثون ⌭")
    zq_lo.loop.run_until_complete(setup_bot())
    LOGS.info("✓ تـم تنزيـل يـــمنثون .. بـنجـاح ✓")
except Exception as e:
    LOGS.error(f"{str(e)}")
    sys.exit()

class RPCheck:
    def __init__(self):
        self.sucess = True
RPcheck = RPCheck()

try:
    LOGS.info("⌭ بـدء إنشـاء البـوت التلقـائـي ⌭")
    zq_lo.loop.run_until_complete(mybot())
    LOGS.info("✓ تـم إنشـاء البـوت .. بـنجـاح ✓")
except Exception as e:
    LOGS.error(f"- {e}")

try:
    LOGS.info("⌭ جـارِ تفعيـل الاشتـراك ⌭")
    zq_lo.loop.create_task(saves())
    LOGS.info("✓ تـم تفعيـل الاشتـراك .. بنجـاح ✓")
except Exception as e:
    LOGS.error(f"- {e}")


async def startup_process():
    await verifyLoggerGroup()
    await load_plugins("plugins")
    await load_plugins("assistant")
    LOGS.info(f"⌔ تـم تنصيـب يـــمنثون . . بنجـاح ✓ \n⌔ لـ إظهـار الاوامـر ارسـل (.الاوامر)")
    await verifyLoggerGroup()
    await add_bot_to_logger_group(BOTLOG_CHATID)
    if PM_LOGGER_GROUP_ID != -100:
        await add_bot_to_logger_group(PM_LOGGER_GROUP_ID)
    await startupmessage()
    RPcheck.sucess = True
    return


zq_lo.loop.run_until_complete(startup_process())

if len(sys.argv) not in (1, 3, 4):
    zq_lo.disconnect()
elif not RPcheck.sucess:
    try:
        zq_lo.run_until_disconnected()
    except ConnectionError:
        pass
else:
    try:
        zq_lo.run_until_disconnected()
    except ConnectionError:
        pass
