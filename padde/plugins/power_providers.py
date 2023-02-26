import hikari
import lightbulb
import miru
import json
from miru.ext import nav
from padde.bot import Padde

class Plugin(lightbulb.Plugin):
    def __init__(self) -> None:
        super().__init__("power_providers")
        self.bot: Padde


plugin = Plugin()


@plugin.command()
@lightbulb.command("show_providers", "Creates embeds showing live prices from providers", guilds=[1079395362869100584])
@lightbulb.implements(lightbulb.SlashCommand)
async def show_providers(ctx: lightbulb.Context) -> None:
    providers = await get_power_providers()
    for p in providers:
        providerEmbed = hikari.Embed(title=f"{p['name']}")
        providerEmbed.add_field("Pricing model:", f"{p['pricingModel']}")
        providerEmbed.add_field("Monthly fee:", f"{p['monthlyFee']}")
        match p['pricingModel']:
            case "fixed":
                providerEmbed.add_field("Fixed price:", f"{p['fixedPrice']}")
                providerEmbed.add_field("Price period:", f"{p['fixedPricePeriod']}")
            case "variable":
                providerEmbed.add_field("Variable price:", f"{p['variablePrice']}")
                providerEmbed.add_field("Price period:", f"{p['variablePricePeriod']}")
            case "spot-hourly":
                providerEmbed.add_field("Hourly spot price:", f"{p['spotPrice']}")
            case "spot-monthly":
                providerEmbed.add_field("Monthly spot price:", f"{p['spotPrice']}")

        await ctx.respond(providerEmbed, flags=hikari.MessageFlag.EPHEMERAL)


async def get_power_providers():
    """
    Retreives live power prices
    :return:
    """
    with open("padde/data/" + "providers.json", 'r') as f:
        return json.load(f)


def load(bot):
    bot.add_plugin(plugin)


def unload(bot):
    bot.remove_plugin(plugin)
