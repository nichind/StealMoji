import asyncio
import discord, json, sqlite3, requests
from discord.ext import commands
from io import BytesIO
from typing import Literal, Optional
from discord.ext.commands import Greedy
from config import *
from discord import app_commands
from utils.utilites import _GetText as _
from utils.utilites import *

class Profile(commands.Cog):
    ''''''
    def __init__(self, client):
        self.client = client

    @commands.hybrid_command(name='invite')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def GetPost(self, ctx):
        '''Get bot invite.'''
        UpdateStats('invite_count', 1)
        if CheckUser(ctx.author.id) is False:
            class SelectMenu(discord.ui.Select):
                def __init__(self):
                    options = [(discord.SelectOption(label='English',
                                                     description='Use english language.')),
                               (discord.SelectOption(label='Русский',
                                                     description='Использовать русский язык.')), ]

                    super().__init__(placeholder='Language', min_values=1, max_values=1,
                                     options=options)

                async def callback(self, interaction: discord.Interaction):
                    if str(self.values[0]) == 'English':
                        AddUser(ctx.author, 'EN')
                        await interaction.response.send_message(_('changed-lang-to-EN', ctx.author.id), ephemeral=True)
                    elif str(self.values[0]) == 'Русский':
                        AddUser(ctx.author, 'RU')
                        await interaction.response.send_message(_('changed-lang-to-RU', ctx.author.id), ephemeral=True)

            view = discord.ui.View()
            view.add_item(item=SelectMenu())
            first_time = discord.Embed(title='', description=f'''
                        *{ctx.author.name}*,
                        Choose your language.
                        Выбери свой язык.
                        ''')
            return await ctx.send(embed=first_time, view=view, ephemeral=True)

        CheckUser(ctx.author.id)

        embed = discord.Embed(title='', description=_('my-invite', ctx.author.id).format(invite=BotSettings.bot_invite,
                                                                                         support=BotSettings.support_server_invite))
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)

        invite = discord.ui.Button(label=_('invite-button', ctx.author.id), style=discord.ButtonStyle.grey,
                                   emoji=Emojis.Buttons.link, url=BotSettings.bot_invite)
        support = discord.ui.Button(label=_('support-button', ctx.author.id), style=discord.ButtonStyle.red,
                                    emoji=Emojis.Buttons.link, url=BotSettings.support_server_invite)
        view = discord.ui.View()
        view.add_item(item=invite)
        view.add_item(item=support)

        await ctx.send(embed=embed, view=view)

    @commands.hybrid_command(name='language')
    @app_commands.describe(
        language='Choose bot language'
    )
    @app_commands.choices(language=[
        app_commands.Choice(name="English", value="EN"),
        app_commands.Choice(name="Русский", value="RU"),
    ])
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def ChangeLanguage(self, ctx, language: app_commands.Choice[str] = None):
        '''Change bot language.'''
        UpdateStats('settings_count', 1)
        if CheckUser(ctx.author.id) is False:
            class SelectMenu(discord.ui.Select):
                def __init__(self):
                    options = [(discord.SelectOption(label='English',
                                                 description='Use english language.')),
                               (discord.SelectOption(label='Русский',
                                                 description='Использовать русский язык.')),]

                    super().__init__(placeholder='Language', min_values=1, max_values=1,
                                     options=options)

                async def callback(self, interaction: discord.Interaction):
                    if str(self.values[0]) == 'English':
                        AddUser(ctx.author, 'EN')
                        await interaction.response.send_message(_('changed-lang-to-EN', ctx.author.id), ephemeral=True)
                    elif str(self.values[0]) == 'Русский':
                        AddUser(ctx.author, 'RU')
                        await interaction.response.send_message(_('changed-lang-to-RU', ctx.author.id), ephemeral=True)

            view = discord.ui.View()
            view.add_item(item=SelectMenu())
            first_time = discord.Embed(title='', description=f'''
                        *{ctx.author.name}*,
                        Choose your language.
                        Выбери свой язык.
                        ''')
            return await ctx.send(embed=first_time, view=view, ephemeral=True)

        if language is not None:
            AddUser(ctx.author.id, language.value)
            await ctx.send(_(f'changed-lang-to-{language.value}', ctx.author.id), ephemeral=True)

    @commands.hybrid_command(name='stats')
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def ChangeLanguage(self, ctx):
        '''See bot stats.'''
        UpdateStats('stats_count', 1)
        if CheckUser(ctx.author.id) is False:
            class SelectMenu(discord.ui.Select):
                def __init__(self):
                    options = [(discord.SelectOption(label='English',
                                                     description='Use english language.')),
                               (discord.SelectOption(label='Русский',
                                                     description='Использовать русский язык.')), ]

                    super().__init__(placeholder='Language', min_values=1, max_values=1,
                                     options=options)

                async def callback(self, interaction: discord.Interaction):
                    if str(self.values[0]) == 'English':
                        AddUser(ctx.author, 'EN')
                        await interaction.response.send_message(_('changed-lang-to-EN', ctx.author.id), ephemeral=True)
                    elif str(self.values[0]) == 'Русский':
                        AddUser(ctx.author, 'RU')
                        await interaction.response.send_message(_('changed-lang-to-RU', ctx.author.id), ephemeral=True)

            view = discord.ui.View()
            view.add_item(item=SelectMenu())
            first_time = discord.Embed(title='', description=f'''
                           *{ctx.author.name}*,
                           Choose your language.
                           Выбери свой язык.
                           ''')
            return await ctx.send(embed=first_time, view=view, ephemeral=True)

        stats = GetStats()
        embed = discord.Embed(title='', description=f'''
Servers: {stats['guild_count']}
Members: {stats['member_count']}
Times steal: {stats['steal_count']}
''')
        await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(Profile(client))
