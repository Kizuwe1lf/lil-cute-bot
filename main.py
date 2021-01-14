import json
import discord
from discord import File
from discord.ext import commands
from discord.ext.commands import has_permissions
from bot_commands.c_compare import compare
from bot_commands.c_osu import get_user1
from bot_commands.c_recent import get_recent1
from bot_commands.c_osutop import *
from bot_commands.c_roll import get_roll_text
from bot_commands.c_map_data import spot_beatmap
from bot_commands.c_ntp import get_ntp
from bot_commands.c_acc import get_acc
from database import *
from bot_commands.c_link import *
from bot_commands.c_leaderboards import *
from secrets import bot_token
from get_user import get_osu_user_from_db
from bot_commands.c_bpp import get_bpp
from bot_commands.c_global import get_global_image
from bot_commands.c_compare_server import get_compare_server_image


# Hey!


def get_prefix(ctx, message):
    with open(r"my_files/server_prefixes.json", "r") as f:
        prefix_list = json.load(f)
    try:
        return prefix_list[str(message.guild.id)]
    except:
        return '>'



bot = commands.Bot(command_prefix=get_prefix)
bot.remove_command('help')


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="osu!"))
    print(f'Logged in as: {bot.user.name}\n')
    print(f'Server List ({len(bot.guilds)})\n')
    server_counter = 1
    for guild in bot.guilds:
        print(f"{server_counter}. {guild.name}")
        server_counter += 1


@bot.command()
@commands.is_owner()
async def memberlist(ctx, rank):
    output = ""
    guild = bot.guilds[int(rank)-1]
    output += f"Server Name: {guild.name}\n"
    output += "Member List \n"
    member_counter = 1
    for member in guild.members:
        if member_counter % 101 == 0:
            await ctx.send(output)
            output = ""
        output += f"{member_counter}. {member} \n"
        member_counter += 1
    await ctx.send(output)


@bot.command()
@commands.is_owner()
async def serverlist(ctx):
    server_list_output = "--------------------\n"
    server_counter = 1
    for guild in bot.guilds:
        server_list_output += f"{server_counter}. {guild.name}\n"
        server_counter += 1
    await ctx.send(server_list_output)


@bot.command()
@commands.is_owner()
async def leaveserver(ctx, rank):
    rank = int(rank) - 1
    try:
        await bot.guilds[rank].leave()
        await ctx.send("Done sir <:hug:627096635658338315>")
    except:
        await ctx.send("I cant <:sadIgnored:530917237406826496>")


@bot.command()
@has_permissions(administrator=True)
async def setprefix(ctx, prefix):
    with open(r"my_files/server_prefixes.json", "r") as f:
        prefix_list = json.load(f)
    prefix_list[str(ctx.guild.id)] = prefix
    with open(r"my_files/server_prefixes.json", "w") as f:
        json.dump(prefix_list, f, indent=4)
    await ctx.send(f"Done new prefix = '{prefix}' for {ctx.guild.name} from now on")


@bot.command()
async def osu(ctx, osu_user: str = None):
    if osu_user == None:
        discord_id = ctx.message.author.id
        osu_user = get_osu_user_from_db(discord_id)
    elif len(osu_user) > 20:
        discord_id = int(osu_user.strip('<@!>'))
        osu_user = get_osu_user_from_db(discord_id)
    if osu_user == 'User not linked':
        await ctx.send('User not linked')
    else:
        output = get_user1(osu_user, ctx.message.author)
        try:
            await ctx.send(content=None, embed=output)
        except:
            await ctx.send(output)


@bot.command(aliases=['r', 'rs'])
async def recent(ctx, osu_user: str = None):
    my_update_bool = False
    if osu_user == None:
        discord_id = ctx.message.author.id
        osu_user = get_osu_user_from_db(discord_id)
        my_update_bool = True
    elif len(osu_user) > 20:
        discord_id = int(osu_user.strip('<@!>'))
        osu_user = get_osu_user_from_db(discord_id)
    if osu_user == 'User not linked':
        await ctx.send('User not linked')
    else:
        output = get_recent1(osu_user, ctx.channel.id, my_update_bool)
        try:
            await ctx.send(content=None, embed=output)
        except:
            await ctx.send(output)


@bot.command(aliases=['compare'])
async def c(ctx, osu_user: str = None):
    if osu_user == None:
        discord_id = ctx.message.author.id
        osu_user = get_osu_user_from_db(discord_id)
    elif len(osu_user) > 20:
        discord_id = int(osu_user.strip('<@!>'))
        osu_user = get_osu_user_from_db(discord_id)
    if osu_user == 'User not linked':
        await ctx.send('User not linked')
    else:
        output = compare(osu_user, ctx.channel.id)
        try:
            if output[2] > 1:
                await send_pages(ctx, output[0], output[1], output[2], bot)
            else:
                await ctx.send(content=None, embed=output[0])
        except:
            await ctx.send(output)


@bot.command()
async def osutop(ctx, osu_user: str = None, p: str = None, play_number: int = 0):
    multi_pages = False
    osu_username = ""
    if osu_user == None or osu_user == 'p' or osu_user == 'r':
        discord_id = ctx.message.author.id
        osu_username = get_osu_user_from_db(discord_id)
    elif len(osu_user) > 20:
        discord_id = int(osu_user.strip('<@!>'))
        osu_username = get_osu_user_from_db(discord_id)
    else:
        osu_username = osu_user
        
    if osu_user == 'p':
        play_number = int(p)
    if osu_user == 'p' or p == 'p':
        output = get_specific_play(osu_username, ctx.message.author, ctx.channel.id, play_number)
    elif osu_user == 'r' or p == 'r':
        output = get_latest_topplays(osu_username, ctx.message.author)
    else:
        output = osu_top(osu_username, ctx.message.author)
        multi_pages = True
    try:
        if multi_pages == True:
            await send_pages(ctx, output[0], output[1], 5, bot)
        else:
            await ctx.send(content=None, embed=output)
    except:
        await ctx.send(output)
    


@bot.command(aliases=['map'])
async def mapdata(ctx, beatmap_id: str =  None):
    output = spot_beatmap(ctx.channel.id, beatmap_id)
    try:
        await ctx.send(embed=output)
    except:
        await ctx.send(output)


@bot.command(aliases=['newtopplay'])
async def ntp(ctx, *p ):
    osu_user = ""
    if p[0].isnumeric():
        discord_id = ctx.message.author.id
        osu_user = get_osu_user_from_db(discord_id)
        pp_tuple = p
    elif len(p[0]) > 20:
        discord_id = int(p[0].strip('<@!>'))
        osu_user = get_osu_user_from_db(discord_id)
        pp_tuple = p[1:]
    else:
        osu_user = p[0]
        pp_tuple = p[1:]
        
    output = get_ntp(osu_user, pp_tuple)
    try:
        await ctx.send(content=None, embed=output)
    except:
        await ctx.send(output)



@bot.command(aliases=['bonuspp'])
async def bpp(ctx, osu_user: str = None):
    if osu_user == None:
        discord_id = ctx.message.author.id
        osu_user = get_osu_user_from_db(discord_id)
    elif len(osu_user) > 20:
        discord_id = int(osu_user.strip('<@!>'))
        osu_username = get_osu_user_from_db(discord_id)
    output = get_bpp(osu_user)
    try:
        await ctx.send(content=None, embed=output)
    except:
        await ctx.send(output)

@bot.command()
async def acc(ctx, accuracy, *mod):
    try:
        accuracy = float(accuracy)
    except:
        await ctx.send("invalid accuracy!")
    if 100 >= accuracy > 49.99:
        if not mod:
            output = get_acc(accuracy, ctx.channel.id)
        else:
            if "ez" in mod[0].lower() and "hr" in mod[0].lower() or "ht" in mod[0].lower() and "dt" in mod[0].lower():
                output = "invalid mods!"
            else:
                output = get_acc(accuracy, ctx.channel.id, mod[0])
        await ctx.send(output)
    else:
        await ctx.send("invalid accuracy!")


@bot.command()
async def leaderboards(ctx):
    output = get_leaderboards(ctx)
    try:
        await ctx.send(content=None, embed=output)
    except:
        await ctx.send(output)


@bot.command()
async def link(ctx, osu_user):
    output = link1(osu_user, ctx.message.author.id)
    await ctx.send(output)


@bot.command()
async def unlink(ctx):
    output = unlink1(ctx.message.author.id)
    await ctx.send(output)

@bot.command()
async def help(ctx):
    await ctx.send(file=File(r"my_files\help.png"))


@bot.command()
async def aliases(ctx):
    await ctx.send(file=File(r"my_files\aliases.png"))


@bot.command()
async def roll(ctx, num=""):
    output = get_roll_text(num)
    await ctx.send(f"{ctx.message.author.name} Just rolled **{output}**")
        


@bot.command()
@commands.is_owner()
async def talkmyboi(ctx, message, channel_id=526881587682344982):
    channel = bot.get_channel(int(channel_id))
    output = message.replace('--', " ")
    await channel.send(output)
    
    
@bot.command(aliases=['global'])
async def g(ctx, mods=""):
    output = get_global_image(ctx.channel.id, mods)
    try:
        await ctx.send(file=File(output))
    except:
        await ctx.send(output)



@bot.command(aliases=['compareserver'])
async def cs(ctx):
    output = get_compare_server_image(ctx)
    try:
        await ctx.send(file=File(output))
    except:
        await ctx.send(output)
    
    
bot.run(bot_token)
