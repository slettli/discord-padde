import datetime
import os
import re

import hikari
import lightbulb
import miru
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv

class Padde(lightbulb.BotApp):
    def __init__(self) -> None:
        load_dotenv()
        super().__init__(token=os.getenv('DISCORD_TOKEN'),
                         intents=hikari.Intents(hikari.Intents.ALL_UNPRIVILEGED | hikari.Intents.MESSAGE_CONTENT | hikari.Intents.GUILDS))

        self.DEVMODE = os.getenv('DEV_MODE')
        self.load_extensions_from("padde/plugins/")  # Load commands
        miru.install(self)