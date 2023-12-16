#(©)Codexbotz

from aiohttp import web
from plugins import web_server

import pyromod.listen
from pyrogram import Client
from pyrogram.enums import ParseMode
import sys
from datetime import datetime

from config import API_HASH, APP_ID, LOGGER, TG_BOT_TOKEN, TG_BOT_WORKERS, FORCE_SUB_CHANNEL, CHANNEL_ID, PORT

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="Bot",
            api_hash=API_HASH,
            api_id=APP_ID,
            plugins={
                "root": "plugins"
            },
            workers=TG_BOT_WORKERS,
            bot_token=TG_BOT_TOKEN
        )
        self.LOGGER = LOGGER

    async def start(self):
        await super().start()
        usr_bot_me = await self.get_me()
        self.uptime = datetime.now()

        if FORCE_SUB_CHANNEL:
            try:
                link = (await self.get_chat(FORCE_SUB_CHANNEL)).invite_link
                if not link:
                    await self.export_chat_invite_link(FORCE_SUB_CHANNEL)
                    link = (await self.get_chat(FORCE_SUB_CHANNEL)).invite_link
                self.invitelink = link
            except Exception as a:
                self.LOGGER(__name__).warning(a)
                self.LOGGER(__name__).warning("Bot can't Export Invite link from Force Sub Channel!")
                self.LOGGER(__name__).warning(f"Please Double check the FORCE_SUB_CHANNEL value and Make sure Bot is Admin in channel with Invite Users via Link Permission, Current Force Sub Channel Value: {FORCE_SUB_CHANNEL}")
                self.LOGGER(__name__).info("\nBot Stopped. Join https://t.me/CodeXBotzSupport for support")
                sys.exit()
        try:
            db_channel = await self.get_chat(CHANNEL_ID)
            self.db_channel = db_channel
            test = await self.send_message(chat_id = db_channel.id, text = "Test Message")
            await test.delete()
        except Exception as e:
            self.LOGGER(__name__).warning(e)
            self.LOGGER(__name__).warning(f"Make Sure bot is Admin in DB Channel, and Double check the CHANNEL_ID Value, Current Value {CHANNEL_ID}")
            self.LOGGER(__name__).info("\nBot Stopped. Join https://t.me/CodeXBotzSupport for support")
            sys.exit()

        self.set_parse_mode(ParseMode.HTML)
        self.LOGGER(__name__).info(f"Bot Running..!\n\nCreated by \nhttps://t.me/HebatLuBoy")
        self.LOGGER(__name__).info(f""" \n\n
FFFFFFFFFFFFFFFFFFFFFF                                  FFFFFFFFFFFFFFFFFFFFFF                                  FFFFFFFFFFFFFFFFFFFFFF                                  MMMMMMMM               MMMMMMMM                    
F::::::::::::::::::::F                                  F::::::::::::::::::::F                                  F::::::::::::::::::::F                                  M:::::::M             M:::::::M                    
F::::::::::::::::::::F                                  F::::::::::::::::::::F                                  F::::::::::::::::::::F                                  M::::::::M           M::::::::M                    
FF::::::FFFFFFFFF::::F                                  FF::::::FFFFFFFFF::::F                                  FF::::::FFFFFFFFF::::F                                  M:::::::::M         M:::::::::M                    
  F:::::F       FFFFFFuuuuuu    uuuuuunnnn  nnnnnnnn      F:::::F       FFFFFFuuuuuu    uuuuuunnnn  nnnnnnnn      F:::::F       FFFFFFooooooooooo   rrrrr   rrrrrrrrr   M::::::::::M       M::::::::::M    eeeeeeeeeeee    
  F:::::F             u::::u    u::::un:::nn::::::::nn    F:::::F             u::::u    u::::un:::nn::::::::nn    F:::::F           oo:::::::::::oo r::::rrr:::::::::r  M:::::::::::M     M:::::::::::M  ee::::::::::::ee  
  F::::::FFFFFFFFFF   u::::u    u::::un::::::::::::::nn   F::::::FFFFFFFFFF   u::::u    u::::un::::::::::::::nn   F::::::FFFFFFFFFFo:::::::::::::::or:::::::::::::::::r M:::::::M::::M   M::::M:::::::M e::::::eeeee:::::ee
  F:::::::::::::::F   u::::u    u::::unn:::::::::::::::n  F:::::::::::::::F   u::::u    u::::unn:::::::::::::::n  F:::::::::::::::Fo:::::ooooo:::::orr::::::rrrrr::::::rM::::::M M::::M M::::M M::::::Me::::::e     e:::::e
  F:::::::::::::::F   u::::u    u::::u  n:::::nnnn:::::n  F:::::::::::::::F   u::::u    u::::u  n:::::nnnn:::::n  F:::::::::::::::Fo::::o     o::::o r:::::r     r:::::rM::::::M  M::::M::::M  M::::::Me:::::::eeeee::::::e
  F::::::FFFFFFFFFF   u::::u    u::::u  n::::n    n::::n  F::::::FFFFFFFFFF   u::::u    u::::u  n::::n    n::::n  F::::::FFFFFFFFFFo::::o     o::::o r:::::r     rrrrrrrM::::::M   M:::::::M   M::::::Me:::::::::::::::::e 
  F:::::F             u::::u    u::::u  n::::n    n::::n  F:::::F             u::::u    u::::u  n::::n    n::::n  F:::::F          o::::o     o::::o r:::::r            M::::::M    M:::::M    M::::::Me::::::eeeeeeeeeee  
  F:::::F             u:::::uuuu:::::u  n::::n    n::::n  F:::::F             u:::::uuuu:::::u  n::::n    n::::n  F:::::F          o::::o     o::::o r:::::r            M::::::M     MMMMM     M::::::Me:::::::e           
FF:::::::FF           u:::::::::::::::uun::::n    n::::nFF:::::::FF           u:::::::::::::::uun::::n    n::::nFF:::::::FF        o:::::ooooo:::::o r:::::r            M::::::M               M::::::Me::::::::e          
F::::::::FF            u:::::::::::::::un::::n    n::::nF::::::::FF            u:::::::::::::::un::::n    n::::nF::::::::FF        o:::::::::::::::o r:::::r            M::::::M               M::::::M e::::::::eeeeeeee  
F::::::::FF             uu::::::::uu:::un::::n    n::::nF::::::::FF             uu::::::::uu:::un::::n    n::::nF::::::::FF         oo:::::::::::oo  r:::::r            M::::::M               M::::::M  ee:::::::::::::e  
FFFFFFFFFFF               uuuuuuuu  uuuunnnnnn    nnnnnnFFFFFFFFFFF               uuuuuuuu  uuuunnnnnn    nnnnnnFFFFFFFFFFF           ooooooooooo    rrrrrrr            MMMMMMMM               MMMMMMMM    eeeeeeeeeeeeee 
                                          """)
        self.username = usr_bot_me.username
        #web-response
        app = web.AppRunner(await web_server())
        await app.setup()
        bind_address = "0.0.0.0"
        await web.TCPSite(app, bind_address, PORT).start()

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("Bot stopped.")
