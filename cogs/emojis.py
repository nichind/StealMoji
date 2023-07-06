import asyncio, requests
import discord, json, sqlite3
from discord.ext import commands
from io import BytesIO
from typing import Literal, Optional
from discord.ext.commands import Greedy
from config import *
from discord import app_commands
from utils.utilites import _GetText as _
from utils.utilites import *

class Emojis(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.hybrid_command(name='steal')
    @commands.has_permissions(manage_emojis=True)
    @commands.guild_only()
    @app_commands.describe(
        emoji='Emoji'
    )
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def Steal(self, ctx, emoji: discord.PartialEmoji):
        '''Clone emoji from other server.'''
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
                        AddUser(ctx.author.id, 'EN')
                        await interaction.response.send_message(_('changed-lang-to-EN', ctx.author.id), ephemeral=True)
                    elif str(self.values[0]) == 'Русский':
                        AddUser(ctx.author.id, 'RU')
                        await interaction.response.send_message(_('changed-lang-to-RU', ctx.author.id), ephemeral=True)

            view = discord.ui.View()
            view.add_item(item=SelectMenu())
            first_time = discord.Embed(title='', description=f'''
            *{ctx.author.name}*,
            Choose your language.
            Выбери свой язык.
            ''')
            return await ctx.send(embed=first_time, view=view, ephemeral=True)

        if emoji.is_custom_emoji():
            emoji_id, server_emojis, work, emj = emoji.id, ctx.guild.emojis, emoji.name, emoji
            emoji = discord.utils.get(server_emojis, id=int(emoji_id))
            if emoji is not None:
                return await ctx.send(_('emoji-from-this-server', ctx.author.id))
            else: emoji = emj
            response = requests.get(emoji.url)
            if response.status_code == 200:
                image_data = response.content
            else:
                return await ctx.send(_('fail-download', ctx.author.id))
            try:
                work = await ctx.guild.create_custom_emoji(name=emoji.name, image=image_data)
            except discord.errors.HTTPException:
                return await ctx.send(_('no-emoji-slots', ctx.author.id))
            except discord.errors.Forbidden:
                return await ctx.send(_('no-perm-to-add-emoji', ctx.author.id))
            UpdateStats('steal_count', 1)
            await ctx.send(_('success-added-emoji', ctx.author.id).format(id=ctx.author.id, emoji=work))
        else:
            return await ctx.send(_('emoji-not-custom', ctx.author.id))

    @commands.hybrid_command(name='remove')
    @commands.has_permissions(manage_emojis=True)
    @commands.guild_only()
    @app_commands.describe(
        emoji='Emoji'
    )
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def Delete(self, ctx, emoji: discord.PartialEmoji):
        '''Remove emoji from server.'''
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
                        AddUser(ctx.author.id, 'EN')
                        await interaction.response.send_message(_('changed-lang-to-EN', ctx.author.id), ephemeral=True)
                    elif str(self.values[0]) == 'Русский':
                        AddUser(ctx.author.id, 'RU')
                        await interaction.response.send_message(_('changed-lang-to-RU', ctx.author.id), ephemeral=True)

            view = discord.ui.View()
            view.add_item(item=SelectMenu())
            first_time = discord.Embed(title='', description=f'''
                *{ctx.author.name}*,
                Choose your language.
                Выбери свой язык.
                ''')
            return await ctx.send(embed=first_time, view=view, ephemeral=True)

        # permissions = discord.Permissions(manage_emojis=True)
        # invite_link = discord.utils.oauth_url(self.client.user.id, permissions=permissions)
        # await ctx.send(f"Invite the bot to your server: {invite_link}")

        if emoji.is_custom_emoji():
            emoji_id, server_emojis, work, emj = emoji.id, ctx.guild.emojis, emoji.name, emoji
            emoji = discord.utils.get(server_emojis, id=int(emoji_id))
            if emoji:
                try:
                    await emoji.delete()
                except discord.errors.Forbidden:
                    return await ctx.send(_('no-perm-to-add-emoji', ctx.author.id))
                UpdateStats('remove_count', 1)
                await ctx.send(_('success-removed-emoji', ctx.author.id).format(id=ctx.author.id, emoji=work))
            else:
                return await ctx.send(_('emoji-from-other-server', ctx.author.id))
        else:
            return await ctx.send(_('emoji-not-custom', ctx.author.id))

async def setup(client):
    await client.add_cog(Emojis(client))