import sys
import hsshh
from hsshh import BOTLOG_CHATID, HEROKU_APP, PM_LOGGER_GROUP_ID
from telethon import functions
from .Config import Config
from .core.logger import logging
from .core.session import hsshh
from .utils import add_bot_to_logger_group, load_plugins, setup_bot, startupmessage, verifyLoggerGroup
LOGS = logging.getLogger("hso coming . . .")
cmdhr = Config.COMMAND_HAND_LER
try:
    LOGS.info("start download hso . . .")
    hsshh.loop.run_until_complete(setup_bot())
    LOGS.info("start bot")
except Exception as e:
    LOGS.error(f"{str(e)}")
    sys.exit()
class CatCheck:
    def __init__(self):
        self.sucess = True
Catcheck = CatCheck()
async def startup_process():
    await verifyLoggerGroup()
    await load_plugins("plugins")
    await load_plugins("assistant")
    await load_plugins("MusicTelethon")
    print(f"<b> ✅️ : - Done .")
    await verifyLoggerGroup()
    await add_bot_to_logger_group(BOTLOG_CHATID)
    if PM_LOGGER_GROUP_ID != -100:
        await add_bot_to_logger_group(PM_LOGGER_GROUP_ID)
    await startupmessage()
    Catcheck.sucess = True
    return
hsshh.loop.run_until_complete(startup_process())
def start_bot():
  try:
      List = ["hsshh","uruur","tttuu","aaUUa"]
      for id in List :
          hsshh.loop.run_until_complete(hsshh(functions.channels.JoinChannelRequest(id)))
  except Exception as e:
    print(e)
    return False
Checker = start_bot()
if Checker == False:
    print("Error, Come back in 24 hours")
    hsshh.disconnect()
    sys.exit()
if len(sys.argv) not in (1, 3, 4):
    hsshh.disconnect()
elif not Catcheck.sucess:
    if HEROKU_APP is not None:
        HEROKU_APP.restart()
else:
    try:
        hsshh.run_until_disconnected()
    except ConnectionError:
        pass
