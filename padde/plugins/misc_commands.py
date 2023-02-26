import hikari
import lightbulb
import miru
from miru.ext import nav
from padde.bot import Padde
from padde.utils.price_chart import ConsumptionChart
from io import BytesIO

class Plugin(lightbulb.Plugin):
    def __init__(self) -> None:
        super().__init__("misc_commands")
        self.bot: Padde


plugin = Plugin()


@plugin.command()
@lightbulb.command("hi", "Hello", guilds=[1079395362869100584])
@lightbulb.implements(lightbulb.SlashCommand)
async def say_hi(ctx: lightbulb.Context) -> None:
    await ctx.respond("Hello!", flags=hikari.MessageFlag.EPHEMERAL)


@plugin.command()
@lightbulb.command("personal_power", "Generates a chart of your power consumption", guilds=[1079395362869100584])
@lightbulb.implements(lightbulb.SlashCommand)
async def personal_power(ctx: lightbulb.Context) -> None:
    plotter = ConsumptionChart('padde/data/consumption.json')
    plotter.gen_plot()
    await ctx.respond(hikari.File('padde/data/power_consumption.png'), flags=hikari.MessageFlag.EPHEMERAL)


def load(bot):
    bot.add_plugin(plugin)


def unload(bot):
    bot.remove_plugin(plugin)
