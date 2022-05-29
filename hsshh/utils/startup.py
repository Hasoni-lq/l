import glob
import os
import sys
import requests
from asyncio.exceptions import CancelledError
from datetime import timedelta
from pathlib import Path
from telethon import Button, functions, types, utils
from hsshh import BOTLOG, BOTLOG_CHATID, PM_LOGGER_GROUP_ID
from ..Config import Config
from ..core.logger import logging
from ..core.session import hsshh
from ..helpers.utils import install_pip
from ..sql_helper.global_collection import del_keyword_collectionlist, get_item_collectionlist
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from .hso import load_module
from .tools import create_supergroup
LOGS = logging.getLogger("hso is coming\n ")
cmdhr = Config.COMMAND_HAND_LER
async def load_plugins(folder):
    path = f"hsshh/{folder}/*.py"
    files = glob.glob(path)
    files.sort()
    for name in files:
        with open(name) as f:
            path1 = Path(f.name)
            shortname = path1.stem
            try:
                if shortname.replace(".py", "") not in Config.NO_LOAD:
                    flag = True
                    check = 0
                    while flag:
                        try:
                            load_module(shortname.replace(".py", ""),  plugin_path=f"hsshh/{folder}")
                            break
                        except ModuleNotFoundError as e:
                            install_pip(e.name)
                            check += 1
                            if check > 5:
                                break
                else:
                    os.remove(Path(f"hsshh/{folder}/{shortname}.py"))
            except Exception as e:
                os.remove(Path(f"hsshh/{folder}/{shortname}.py"))
                LOGS.info(f"error with {shortname} because : {e}"                )
async def startupmessage():
    try:
        if BOTLOG:
            Config.CATUBLOGO = await hsshh.tgbot.send_file(BOTLOG_CHATID, "https://telegra.ph/file/876adbae077148af2672b.jpg", caption="🇮🇶 ⦙ تم اعادة التشغيل ✓\n السورس الخاص بك  :  [ 7.6 ] .\n\n♛ ⦙ للحصول على اوامر السورس\n أرسل : (  `.الاوامر`  )",                buttons=[(Button.url("المطور", "tg://settings"),)],            )
    except Exception as e:
        LOGS.error(e)
        return None
async def add_bot_to_logger_group(chat_id):
    bot_details = await hsshh.tgbot.get_me()
    try:
        await hsshh(            functions.messages.AddChatUserRequest(                chat_id=chat_id,                user_id=bot_details.username,                fwd_limit=1000000            )        )
    except BaseException:
        try:
            await hsshh(
                functions.channels.InviteToChannelRequest(                    channel=chat_id,                    users=[bot_details.username]                )            )
        except Exception as e:
            LOGS.error(str(e))
async def setup_bot():
    try:
        await hsshh.connect()
        config = await hsshh(functions.help.GetConfigRequest())
        for option in config.dc_options:
            if option.ip_address == hsshh.session.server_address:
                if hsshh.session.dc_id != option.id:
                    LOGS.warning(                        f"it is will {hsshh.session.dc_id}"                        f"♛ ︙with {option.id}"                    )
                hsshh.session.set_dc(option.id, option.ip_address, option.port)
                hsshh.session.save()
                break
        bot_details = await hsshh.tgbot.get_me()
        Config.TG_BOT_USERNAME = f"@{bot_details.username}"
        # await hsshh.start(bot_token=Config.TG_BOT_USERNAME)
        hsshh.me = await hsshh.get_me()
        hsshh.uid = hsshh.tgbot.uid = utils.get_peer_id(hsshh.me)
        if Config.OWNER_ID == 0:
            Config.OWNER_ID = utils.get_peer_id(hsshh.me)
    except Exception as e:
        LOGS.error(f"termix code is error : {str(e)}")
        sys.exit()
async def verifyLoggerGroup():
    flag = False
    if BOTLOG:
        try:
            entity = await hsshh.get_entity(BOTLOG_CHATID)
            if not isinstance(entity, types.User) and not entity.creator:
                if entity.default_banned_rights.send_messages:
                    LOGS.info(                        "error without: PRIVATE_GROUP_BOT_API_ID is."                    )
                if entity.default_banned_rights.invite_users:
                    LOGS.info(                        "error without: PRIVATE_GROUP_BOT_API_ID is."                    )
        except ValueError:
            LOGS.error("Check out the group : PRIVATE_GROUP_BOT_API_ID.")
        except TypeError:
            LOGS.error(                "this group is error please check it out : PRIVATE_GROUP_BOT_API_ID. ."            )
        except Exception as e:
            LOGS.error(                "An error occurred Check your group : PRIVATE_GROUP_BOT_API_ID.\n"                + str(e)            )
    else:
        descript = "اذا تحذف هذا الكروب السورس راح يروح حبي"
        iqphoto1 = await hsshh.upload_file(file="photos/group/hsshh1.jpg")
        _, groupid = await create_supergroup(            "كروب التخزين العام", hsshh, Config.TG_BOT_USERNAME, descript  ,  iqphoto1 )
        addgvar("PRIVATE_GROUP_BOT_API_ID", groupid)
        print("done create group.")
        flag = True
    if PM_LOGGER_GROUP_ID != -100:
        try:
            entity = await hsshh.get_entity(PM_LOGGER_GROUP_ID)
            if not isinstance(entity, types.User) and not entity.creator:
                if entity.default_banned_rights.send_messages:
                    LOGS.info(                        "error without: PM_LOGGER_GROUP_ID is."                    )
                if entity.default_banned_rights.invite_users:
                    LOGS.info(                        "error without: PM_LOGGER_GROUP_ID is."                    )
        except ValueError:
            LOGS.error("error without:  PM_LOGGER_GROUP_ID. .")
        except TypeError:
            LOGS.error("this : PM_LOGGER_GROUP_ID .")
        except Exception as e:
            LOGS.error(                "error without:  PM_LOGGER_GROUP_ID.\n" + str(e)            )
    else:
        descript = "شوف حبي، هذا الكروب يحفظ الرسائل الي تجيك بكيفك اذا تريد تحذفه لو لا"
        iqphoto2 = await hsshh.upload_file(file="photos/group/hsshh2.jpg")
        _, groupid = await create_supergroup(            "تخزين الخاص", hsshh, Config.TG_BOT_USERNAME, descript    , iqphoto2  )
        addgvar("PM_LOGGER_GROUP_ID", groupid)
        print("done create group. PRIVATE_GROUP_BOT_API_ID .")
        flag = True
    if flag:
        executable = sys.executable.replace(" ", "\\ ")
        args = [executable, "-m", "hsshh"]
        os.execle(executable, *args, os.environ)
        sys.exit(0)
