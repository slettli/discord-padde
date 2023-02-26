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
        self.vendor_message = (0, 0)

    def schedule_vendor_updates(self, messageID, providerName):
        scheduler = AsyncIOScheduler()
        scheduler.add_job(self.update_vendor_price, 'interval', args=(messageID, providerName), minutes=1)
        scheduler.start()

    async def update_vendor_price(self, messageID, provider):
        # Update timestamp
        editedMessage = await self.rest.fetch_message(self.vendor_message[0], self.vendor_message[1])
        editedMessage = re.sub(r'\(.*?\)', f"(<t:{round(datetime.datetime.now().timestamp())}:f>)", editedMessage.content)
        await self.rest.edit_message(channel=self.vendor_message[0], message=self.vendor_message[1], content=editedMessage)
        # Update vendor embed with pricing
        # Joke, there's nothing to update and therefore no code for that at the moment :)
