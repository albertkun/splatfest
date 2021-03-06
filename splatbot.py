import discord
from dconfig import DConfig
from discord.ext import commands
from datetime import datetime
import random
from peewee import *
from models import *
from pytz import timezone
import pytz

bot = commands.Bot(command_prefix='!')
# Bring in your discord bot key
TOKEN = DConfig.KEY

@bot.event
async def on_ready():
    print("The bot is ready!")
    await bot.change_presence(activity=discord.Game(name="the splatfest"))

@bot.command(aliases=['m','go'])
async def match(ctx):
    fest_id = 1
    channel = bot.get_channel(609554010294452235)
    possible_responses = [
        'Regular Match',
        '2x Match',
        '4x Match!!!',
    ]
    result = random.choices(possible_responses,[0.80, 0.15, 0.05], k=1)
    t = datetime.now()
    timeid = int((t-datetime(1970,1,1)).total_seconds())
    match_query = Match.select().count()
    print(match_query)
    match_id = match_query+1
    the_outcome = result[0]
    print(the_outcome)
    if the_outcome == '4x Match!!!':
        modifier = 4
    if the_outcome == '2x Match':
        modifier = 2
    if the_outcome == 'Regular Match':
        modifier = 1
    date = datetime.today().strftime('%Y-%m-%d')
    time = datetime.today().strftime('%H:%M:%S')
    host = ctx.message.author
    nickname = ctx.message.https://discord.gg/hEDCnUauthor.name
    print(host)

    date_format='%H:%M:%S %Z'
    date_f = datetime.now(tz=pytz.utc)
    date_f = date_f.astimezone(timezone('US/Pacific'))
    match = Match(fest_id=fest_id,match_id=match_id,modifier=modifier,date=date,time=time,host=host)
    match.save(force_insert=True)
    await ctx.send(str(the_outcome)+" that "+str(nickname)+" is hosting at "+str(date_f.strftime(date_format))+".")
    
