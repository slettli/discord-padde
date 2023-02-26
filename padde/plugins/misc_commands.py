import hikari
import lightbulb
import miru
from miru.ext import nav
from padde.bot import Padde
from padde.utils.price_chart import ConsumptionChart

class Plugin(lightbulb.Plugin):
    def __init__(self) -> None:
        super().__init__("misc_commands")
        self.bot: Padde


plugin = Plugin()


class PersonalConsumptionView(miru.View):
    """
    Lets user select and view power pricing for a region using a drop-down menu
    """
    def __init__(self):
        super().__init__(timeout=None)

    @miru.button(label="Show personal consumption", style=hikari.ButtonStyle.PRIMARY, custom_id="personal_power_button")
    async def tomorrow_button(self, button: miru.Button, ctx: miru.ViewContext) -> None:
        await ctx.defer()
        plotter = ConsumptionChart('padde/data/consumption.json')
        plotter.gen_plot()
        await ctx.respond(hikari.File('padde/data/images/power_consumption.png'), flags=hikari.MessageFlag.EPHEMERAL)


@plugin.listener(hikari.StartedEvent)
async def startup_misc_views(event: hikari.StartedEvent) -> None:
    """
    Reinstates previously posted views when bot starts
    """
    pcc_view = PersonalConsumptionView()
    await pcc_view.start()


@plugin.command()
@lightbulb.command("personal_power_button", "Spawn button to show personal power usage", guilds=[1079395362869100584])
@lightbulb.implements(lightbulb.SlashCommand)
async def show_power_prices(ctx: lightbulb.Context) -> None:
    pcView = PersonalConsumptionView()
    acResp = await plugin.bot.rest.create_message(ctx.channel_id, content="See personal power usage.\n", components=pcView)
    await pcView.start(acResp)
    await ctx.respond("Done.", flags=hikari.MessageFlag.EPHEMERAL, delete_after=10)


@plugin.command()
@lightbulb.command("hi", "Hello", guilds=[1079395362869100584])
@lightbulb.implements(lightbulb.SlashCommand)
async def say_hi(ctx: lightbulb.Context) -> None:
    await ctx.respond("Hello!", flags=hikari.MessageFlag.EPHEMERAL)


def load(bot):
    bot.add_plugin(plugin)


def unload(bot):
    bot.remove_plugin(plugin)
