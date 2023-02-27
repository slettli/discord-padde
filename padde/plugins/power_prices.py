import os
import datetime
import aiohttp
import hikari
import lightbulb
import miru
import json
import matplotlib.pyplot as plt
from miru.ext import nav
from padde.bot import Padde
from datetime import datetime, timedelta
from matplotlib.dates import DateFormatter, HourLocator


class Plugin(lightbulb.Plugin):
    def __init__(self) -> None:
        super().__init__("power_providers")
        self.bot: Padde
        self.last_region = "NO1"


plugin = Plugin()


class PowerPricesView(miru.View):
    """
    Lets user select and view power pricing for a region using a drop-down menu
    """
    def __init__(self):
        super().__init__(timeout=None)

    @miru.text_select(
        options=[
            miru.SelectOption(
                label="Bergen / Vest-Norge",
                value="NO5",
            ),
            miru.SelectOption(
                label="Kristiansand / Sør-Norge",
                value="NO2",
            ),
            miru.SelectOption(
                label="Oslo / Øst-Norge",
                value="NO1",
            ),
            miru.SelectOption(
                label="Trondheim / Midt-Norge",
                value="NO3",
            ),
            miru.SelectOption(
                label="Tromsø / Nord-Norge",
                value="NO4",
            )
        ],
        placeholder="Select region",
        custom_id="power_region_selector_list"
    )
    async def basic_select(self, select: miru.TextSelect, ctx: miru.ViewContext) -> None:
        """
        Fetches today's power prices for selected region, generates and posts a plot.
        """
        await ctx.defer(flags=hikari.MessageFlag.EPHEMERAL)
        plugin.last_region = select.values[0]

    async def create_chartid(self, regionCode, when):
        now = datetime.now()

        match when:
            case 0:  # Show prices for yesterday
                now = now - timedelta(days=1)
            case 2:  # Show prices for yesterday
                now = now + timedelta(days=1)
            case _:
                pass

        # Pick text for chosen region
        match regionCode:
            case "NO1":
                region = "Oslo / Øst-Norge"
            case "NO2":
                region = "Kristiansand / Sør-Norge"
            case "NO3":
                region = "Trondheim / Midt-Norge"
            case "NO4":
                region = "Tromsø / Nord-Norge"
            case _:
                region = "Bergen / Vest-Norge"

        return f"{regionCode}-{now.year}-{str(now.month).zfill(2)}-{str(now.day).zfill(2)}"

    async def create_graph(self, regionCode, when):

        now = datetime.now()

        match when:
            case 0:  # Show prices for yesterday
                now = now - timedelta(days=1)
            case 2:  # Show prices for yesterday
                now = now + timedelta(days=1)
            case _:
                pass

        # Pick text for chosen region
        match regionCode:
            case "NO1":
                region = "Oslo / Øst-Norge"
            case "NO2":
                region = "Kristiansand / Sør-Norge"
            case "NO3":
                region = "Trondheim / Midt-Norge"
            case "NO4":
                region = "Tromsø / Nord-Norge"
            case _:
                region = "Bergen / Vest-Norge"

        chartid = f"{regionCode}-{now.year}-{str(now.month).zfill(2)}-{str(now.day).zfill(2)}"

        if os.path.isfile(f"padde/data/images/{chartid}.png"):  # Check if file already exists (chart has been made)
            return region

        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://www.hvakosterstrommen.no/api/v1/prices/{now.year}/{str(now.month).zfill(2)}-{str(now.day).zfill(2)}_{regionCode}.json") as r:
                data = await r.json()

        # Extract relevant values from data
        prices = [d['NOK_per_kWh'] for d in data]
        times = [d['time_start'] for d in data]

        # Convert times to datetime objects
        times = [datetime.fromisoformat(t) for t in times]

        # Create plot
        fig, ax = plt.subplots()
        ax.plot(times, prices)

        # Set the x-axis tick locator and formatter
        locator = HourLocator(byhour=[0, 5, 10, 15, 20])
        formatter = DateFormatter('%H:%M')
        ax.xaxis.set_major_locator(locator)
        ax.xaxis.set_major_formatter(formatter)

        # Annotate highest and lowest points
        min_price = min(prices)
        max_price = max(prices)
        min_time = times[prices.index(min_price)]
        max_time = times[prices.index(max_price)]
        ax.annotate(f'{int(min_price * 100)} øre/kWh, {min_time.hour}:00', xy=(min_time, min_price),
                    xytext=(min_time + timedelta(hours=1), min_price - 0.01))
        ax.annotate(f'{int(max_price * 100)} øre/kWh, {max_time.hour}:00', xy=(max_time, max_price),
                    xytext=(max_time + timedelta(hours=-1), max_price + 0.01))


        # Set axis labels and title
        ax.set_ylabel('Price (øre/kWh)')
        ax.set_title(f"Prices for {region}, {now.year}/{str(now.month).zfill(2)}-{str(now.day).zfill(2)}")

        # Save plot as png
        plt.savefig(f'padde/data/images/{chartid}.png')
        plt.clf()

        return region

    @miru.button(label="Yesterday", style=hikari.ButtonStyle.PRIMARY, custom_id="power_yesterday_button")
    async def yesterday_button(self, button: miru.Button, ctx: miru.ViewContext) -> None:
        await ctx.defer()
        chartid = await self.create_chartid(plugin.last_region, 0)
        region = await self.create_graph(plugin.last_region, 0)
        await ctx.respond(content=f"Yesterday's prices for {region}:", attachment=hikari.File(f'padde/data/images/{chartid}.png'), flags=hikari.MessageFlag.EPHEMERAL)

    @miru.button(label="Today", style=hikari.ButtonStyle.PRIMARY, custom_id="power_today_button")
    async def today_button(self, button: miru.Button, ctx: miru.ViewContext) -> None:
        await ctx.defer()
        chartid = await self.create_chartid(plugin.last_region, 1)
        region = await self.create_graph(plugin.last_region, 1)
        await ctx.respond(content=f"Today's prices for {region}:", attachment=hikari.File(f'padde/data/images/{chartid}.png'), flags=hikari.MessageFlag.EPHEMERAL)

    @miru.button(label="Tomorrow", style=hikari.ButtonStyle.PRIMARY, custom_id="power_tomorrow")
    async def tomorrow_button(self, button: miru.Button, ctx: miru.ViewContext) -> None:
        await ctx.defer()
        chartid = await self.create_chartid(plugin.last_region, 2)
        region = await self.create_graph(plugin.last_region, 2)
        await ctx.respond(content=f"Tomorrow's prices for {region}:", attachment=hikari.File(f'padde/data/images/{chartid}.png'), flags=hikari.MessageFlag.EPHEMERAL)


@plugin.listener(hikari.StartedEvent)
async def startup_views(event: hikari.StartedEvent) -> None:
    """
    Reinstates previously posted views when bot starts
    """
    pc_view = PowerPricesView()
    await pc_view.start()


@plugin.command()
@lightbulb.command("power_prices", "Creates embeds showing offers from providers", guilds=[1079395362869100584])
@lightbulb.implements(lightbulb.SlashCommand)
async def show_power_prices(ctx: lightbulb.Context) -> None:
    pView = PowerPricesView()
    aResp = await plugin.bot.rest.create_message(ctx.channel_id, content="Select a region to view today's prices.\n"
                                                                         "Power prices delivered by hvakosterstrommen.no", components=pView)
    await pView.start(aResp)
    await ctx.respond("Done.", flags=hikari.MessageFlag.EPHEMERAL, delete_after=10)


def load(bot):
    bot.add_plugin(plugin)


def unload(bot):
    bot.remove_plugin(plugin)
