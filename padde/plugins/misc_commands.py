import hikari
import lightbulb
import miru
from miru.ext import nav
from padde.bot import Padde

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


def load(bot):
    bot.add_plugin(plugin)


def unload(bot):
    bot.remove_plugin(plugin)
