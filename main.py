import asyncio
import discord
import json, os
from discord.ext import commands
from config import *
from discord.ext.commands import Greedy
from typing import Literal, Optional
from utils.utilites import *
from utils.utilites import _GetText as _

intents = discord.Intents.default()

class Client(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix='!',
            intents = intents,
            application_id = BotSettings.application_id
        )

    async def on_ready(self):
        await client.change_presence(activity=discord.Game(name=BotSettings.status))
        client.tree.copy_global_to(guild=discord.Object(id=BotSettings.support_server))

        print('Client ready.')

        permissions = discord.Permissions(manage_emojis=True)
        invite_link = discord.utils.oauth_url(client.user.id, permissions=permissions)
        print(f"{invite_link}")
        # if BotSettings.status_roll_active:
        #     while True:
        #         for status in StatusRoll.Statuses:

        while True:
            guild_count = len(client.guilds)
            member_count = sum(guild.member_count for guild in client.guilds)

            UpdateStats('guild_count', guild_count, True)
            UpdateStats('member_count', member_count, True)
            await asyncio.sleep(60)

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"{Emojis.Events.error} {_('error-command-on-cooldown', ctx.author.id).format(round(error.retry_after, 2))}")
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send(f"{Emojis.Events.error} {_('error-user-not-found', ctx.author.id)}")
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send(f"{Emojis.Events.error} {_('error-bot-no-perms', ctx.author.id)}")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(f"{Emojis.Events.error} {_('error-no-permission', ctx.author.id)}")
        elif isinstance(error, discord.ext.commands.errors.CommandNotFound):
            await ctx.send(f"{Emojis.Events.error} {_('error-command-not-found', ctx.author.id)}")
        elif isinstance(error, discord.ext.commands.errors.PartialEmojiConversionFailure):
            await ctx.send(f"{Emojis.Events.error} {_('error-not-emoji', ctx.author.id)}")
        else:
            await ctx.send(f"{Emojis.Events.error} {_('error-unknown', ctx.author.id).format(error)}")

    async def on_guild_join(self, guild):
        print('NEW GUILD', f'ID: {guild.id}, NAME: {guild}')

    async def setup_hook(self):
        print(f"\033[31mLogged in as {client.user}\033[39m")
        cogs_folder = f"{os.path.abspath(os.path.dirname(__file__))}/cogs"
        for filename in os.listdir(cogs_folder):
            if filename.endswith(".py"):
                await client.load_extension(f"cogs.{filename[:-3]}")
        await client.tree.sync()

client = commands.Bot(command_prefix='!', intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents)

client = Client()


client.run(BotSettings.token)