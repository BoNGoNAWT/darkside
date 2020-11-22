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
async def on_voice_state_update(member,before,after):
    if after.channel.id == 731829827065348119:
        for guild in Bot.guilds:
            maincategory = discord.utils.get(guild.categories, id=731829695045173278)
            channel2 = await guild.create_voice_channel(name=f"Канал {member.display_name}",category = maincategory)
            await channel2.set_permissions(member,connect=True,mute_members=True,move_members=True,manage_channels=True)
            await member.move_to(channel2)
            def check(x,y,z):
                return len(channel2.members) == 0
            await Bot.wait_for('voice_state_update',check=check)
            await channel2.delete()



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


@Bot.command()
@commands.has_permissions(manage_messages =True)
async def say(ctx, *, msg):
    await ctx.message.delete()
    await ctx.send("{}".format(msg))
 
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
    
@Bot.event
async def on_raw_reaction_add(payload):
    message_id == payload.message_id
    if message_id == 779988307395477514:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, Bot.guilds)
        
        if payload.emoji.name == 'one':
            role = discord.utils.get(guild.roles, name='ghost')
        elif payload.emoji.name == 'two':
            role = discord.utils.get(guild.roles, name='flame')
        elif payload.emoji.name == 'three':
            role = discord.utils.get(guild.roles, name='dark')
            
        else:
            role = discord.utils.get(guild.roles, name=payload.emoji.name)

        if role is not None:
            member = discord.utils.find(lambda m: m.id ==- payload.user_id, guild.members)
            if member is not None:
                await member.add_roles(role)
            else:
                print('Member not found')
        else:
            print('Role not found')
    
    
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
