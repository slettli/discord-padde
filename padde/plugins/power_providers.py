import datetime

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
@lightbulb.command("provider_offers", "Creates embeds showing offers from providers", guilds=[1079395362869100584])
@lightbulb.implements(lightbulb.SlashCommand)
async def show_providers(ctx: lightbulb.Context) -> None:
    if plugin.bot.vendor_message == (0, 0):  # Create new timestamp and save IDs for later updating
        messageStamp = await plugin.bot.rest.create_message(ctx.channel_id, f"Prices were last updated at: (<t:{round(datetime.datetime.now().timestamp())}:f>)")
        plugin.bot.vendor_message = (messageStamp.channel_id, messageStamp.id)
        plugin.bot.schedule_vendor_updates(0, "")

    providers = await get_power_providers()
    for p in providers:
        providerEmbed = hikari.Embed(title=f"{p['name']}")
        providerEmbed.add_field("Pricing model:", f"{p['pricingModel']}")
        providerEmbed.add_field("Monthly fee:", f"{p['monthlyFee']}")
        match p['pricingModel']:
            case "fixed":
                providerEmbed.add_field("Fixed price:", f"{p['fixedPrice']}")
                providerEmbed.add_field("Price period:", f"{p['fixedPricePeriod']} months")
            case "variable":
                providerEmbed.add_field("Variable price:", f"{p['variablePrice']}")
                providerEmbed.add_field("Price period:", f"{p['variablePricePeriod']} months")
            case "spot-hourly":
                providerEmbed.add_field("Hourly spot price:", f"{p['spotPrice']}/kWh")
            case "spot-monthly":
                providerEmbed.add_field("Monthly spot price:", f"{p['spotPrice']}/kWh")

        message = await plugin.bot.rest.create_message(ctx.channel_id, providerEmbed)


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
