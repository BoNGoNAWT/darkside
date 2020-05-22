import discord
from discord.ext import commands
import random
from discord.utils import get
import shutil
import json
import asyncio
import youtube_dl
import os
from itertools import cycle
import colorsys
from discord import Game, Embed, Color, Status, ChannelType
import datetime


Bot = commands.Bot(command_prefix = ".")

Bot.remove_command('help')





@Bot.event
async def on_ready():
    print('Bot online!')




@Bot.event
async def on_command_error(ctx, error):
    pass



@Bot.event
async def on_member_join(member):
    channel = Bot.get_channel(580775363601235989)
    Bot.load_extension('cogs.music')
    role = discord.utils.get(member.guild.roles, id = 581177746475057153)

    emb = discord.Embed(title = 'Join', colour = discord.Color.dark_magenta())

    emb.set_author(name = member.name, icon_url = member.avatar_url)
    emb.add_field(name = 'Пополнение', value = 'К нам присоединился {}'.format(member.mention))
    

    await member.add_roles(role)
    await channel.send(embed = emb)
    

@Bot.command(pass_context= True)
@commands.has_permissions(manage_messages =True)
async def clear(ctx, amount = 100):
    await ctx.channel.purge(limit = amount)

@Bot.command(pass_context = True)
@commands.has_permissions(administrator = True)

async def kick(ctx, member: discord.Member, *, reason = None):
    await ctx.channel.purge(limit = 1)
    emb = discord.Embed(title = 'Kick', colour = discord.Color.purple())

    await member.kick(reason = reason)
    emb.set_author(name = member.name, icon_url = member.avatar_url)
    emb.add_field(name = 'Kick', value = 'Пинком был изгнан {}'.format(member.mention))
    await ctx.send(embed = emb)
    await member.send(embed = discord.Embed(title = 'Вас выгнали с сервера Dark Side!', colour = discord.Color.purple()))

@Bot.command(pass_context = True)
@commands.has_permissions(administrator = True)

async def ban(ctx, member: discord.Member, *, reason = None):
    await ctx.channel.purge(limit = 1)
    emb = discord.Embed(title = 'Ban', colour = discord.Color.red())
    

    await member.ban(reason = reason)

    emb.set_author(name = member.name, icon_url = member.avatar_url)
    emb.add_field(name = 'Banned', value = 'Великая печать изгнания возложена на {}'.format(member.mention))
    emb.set_footer(text = 'Был забанен администратором {}'.format(ctx.author.name), icon_url = ctx.author_url)
    await ctx.send(embed = emb)
    await member.send(embed = discord.Embed(title = 'Вы были забанены администратором{}'.format(ctx.author.name), icon_url = ctx.author_url, colour = discord.Color.red()))

@Bot.command(pass_context= True)
@commands.has_permissions(administrator = True)

async def unban(ctx, *, member):
    await ctx.channel.purge(limit = 1)

    banned_users = await ctx.guild.bans()


    for ban_entry in banned_users:
        user = ban_entry.user
        emb = discord.Embed(title = 'Unban', colour = discord.Color.green())


        await ctx.guild.unban(user)
        emb.set_author(name = member.name)
        
        await ctx.send(f'Великая печать бана снята с {user.menttion}')

        return

@Bot.command(pass_context= True)


async def help(ctx):
    emb = discord.Embed(title = 'Команды:')

    emb.add_field(name = 'clear', value = 'Очичтка чата')
    emb.add_field(name = 'kick', value = 'Выгнать участника с сервера')
    emb.add_field(name = 'ban', value = 'Забанить участника')
    emb.add_field(name = 'unban', value = 'Розбанить участника')

    await ctx.send(embed = emb)

@Bot.command()
async def say(ctx, *, msg):
    await ctx.message.delete()
    await ctx.send("{}".format(msg))

@Bot.command()
async def ping(ctx):
    await ctx.send("Pong")

@ban.error
async def error_command(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(embed = discord.Embed(title = '{} у вас недостаточно прав!'.format(ctx.author.name), colour = discord.Color.red()))
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(embed = discord.Embed(title = '{} укажите аргумент!'.format(ctx.author.name), colour = discord.Color.red()))

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(embed = discord.Embed(title = '{} у вас недостаточно прав!'.format(ctx.author.name), colour = discord.Color.red()))
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(embed = discord.Embed(title = '{} укажите аргумент!'.format(ctx.author.name), colour = discord.Color.red()))




token = os.environ.get('BOT_TOKEN')
Bot.run(str(token))
