import discord
from discord.ext import commands
import random
from discord.utils import get
import shutil
import json
import asyncio
import os
from itertools import cycle
import colorsys
from discord import Game, Embed, Color, Status, ChannelType
import datetime
import sqlite3
import math
import sys, traceback
import time
from datetime import timedelta
from collections import OrderedDict, deque, Counter

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
    role = discord.utils.get(member.guild.roles, id=int('581177746475057153'))
    await member.add_roles(role)
    guild=member.guild
    mention=member.mention

    embed = discord.Embed(title=str("-===New User===-"), colour=discord.Color.blurple(), description=str('{} joined of this server'.format(mention)))
    embed.set_thumbnail(url=f"{member.avatar_url}")
    embed.set_author(name=f"{member.name}", icon_url=f"{member.guild.icon_url}")
    embed.timestamp = datetime.datetime.utcnow()
    embed.add_field(name='ID :', value=member.id)
    embed.add_field(name='Никнейм :', value=member.display_name)
    embed.add_field(name='Количество людей :', value=len(list(guild.members)))
    embed.add_field(name='В дискорде с :', value=member.created_at.strftime("%a %#b %B %Y, %I:%M %p UTC"))
    embed.add_field(name='Присоединился к нам :', value=member.joined_at.strftime("%a %#b %B %Y, %I:%M %p UTC"))

    channel = discord.utils.get(member.guild.channels, id=int("580775363601235989"))
    await channel.send(embed=embed)


@Bot.command(pass_context= True)
@commands.has_permissions(manage_messages =True)
async def clear(ctx, amount = 100):
    await ctx.channel.purge(limit = amount)


@Bot.command()
async def meme(ctx, msg):
    images=["https://www.google.com/search?q=мемы&tbm=isch&ved=2ahUKEwiW6qDlgPDpAhVKsyoKHdP3A1IQ2-cCegQIABAA&oq=мемы&gs_lcp=CgNpbWcQAzIHCAAQsQMQQzIHCAAQsQMQQzIHCAAQsQMQQzIECAAQQzIECAAQQzIECAAQQzIECAAQQzIECAAQQzIFCAAQsQMyBQgAELEDOgQIIxAnOgIIAFCX9QJYxYADYKuEA2gAcAB4AIABY4gB0wKSAQE0mAEAoAEBqgELZ3dzLXdpei1pbWc&sclient=img&ei=_QXdXtb3IcrmqgHT74-QBQ&bih=751&biw=1495&client=opera-gx&hs=YV0"]

    embed=discord.Embed(colour=discord.Colour.orange())

    embed.set_image(url=random.choice(images))

    await ctx.send(embed=embed)

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
    emb.add_field(name = 'say', value = 'Отправить сообщение от имени бота')
    emb.add_field(name = 'send', value = 'Отправить личное сообщение от имени бота')
    emb.add_field(name = 'fck', value = 'Послать к трём чертям')
    emb.add_field(name = 'hug', value = 'Обнять')
    emb.add_field(name = 'kiss', value = 'Поцеловать')
    emb.add_field(name = 'kill', value = 'Убить')

    await ctx.send(embed = emb)

@Bot.command()
@commands.has_permissions(manage_messages =True)
async def say(ctx, *, msg):
    await ctx.message.delete()
    await ctx.send("{}".format(msg))

@Bot.command()
async def fck(ctx, member: discord.Member):
    await ctx.message.delete()
    await ctx.send(f"{ctx.author.mention} послал к трём чертям {member.mention}")


@Bot.command()
async def hug(ctx, member: discord.Member):
    await ctx.message.delete()
    await ctx.send(f"{ctx.author.mention} обнял(а) {member.mention}")

@Bot.command()
async def kiss(ctx, member: discord.Member):
    await ctx.message.delete()
    await ctx.send(f"{ctx.author.mention} поцеловал(а) {member.mention}")

@Bot.command()
async def kill(ctx, member: discord.Member):
    await ctx.message.delete()
    await ctx.send(f"{ctx.author.mention} убил (а) {member.mention}")
 

@Bot.command()
@commands.has_permissions( administrator = True)
async def send(ctx, member: discord.Member, *, msg):
    await ctx.message.delete()
    await member.send('{}'.format(msg))
    await ctx.send('Сообщение отправлено')
    


@Bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

@Bot.command()
async def king(ctx):
    await ctx.send("Kong!")

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