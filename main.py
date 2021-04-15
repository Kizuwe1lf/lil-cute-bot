import json
import discord
import os
from dotenv import load_dotenv, find_dotenv
from discord import File
from discord.ext import commands
from discord.ext.commands import has_permissions

# my files

from bot_commands.c_osu import commands_osu
from bot_commands.c_recent import commands_recent
from bot_commands.c_compare import commands_compare
from bot_commands.c_osutop import commands_osutop, commands_osutop_r, commands_osutop_p
from bot_commands.c_link_unlink import commands_link, commands_unlink
from bot_commands.c_ntp import commands_ntp
from bot_commands.c_bpp import commands_bpp
from bot_commands.c_acc import commands_acc
from bot_commands.c_map import commands_map
from bot_commands.c_leaderboards import commands_leaderboards
from bot_commands.c_global import commands_global
from bot_commands.c_compare_server import commands_compare_server
from bot_commands.c_roll import commands_roll
from database import Database
from scripts import get_osu_username_from_param

# Hey!


def get_prefix(ctx, message):
    db_obj = Database()
    return db_obj.get_prefix(message.guild.id)[0]


bot = commands.Bot(command_prefix=get_prefix)
bot.remove_command('help')


@bot.command()
@has_permissions(administrator=True)
async def setprefix(ctx, prefix):
    db_obj = Database()
    db_prefix = db_obj.set_prefix(ctx.guild.id, prefix)
    await ctx.send(f"Done new prefix = '{db_prefix}' for {ctx.guild.name} from now on")


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
async def osu(ctx, player: str = None):
    db_obj = Database()
    player, null = get_osu_username_from_param(ctx, player, db_obj)
    await commands_osu(ctx, player)


@bot.command(aliases=['r', 'rs'])
async def recent(ctx, player: str = None):
    db_obj = Database()
    player, update_bool = get_osu_username_from_param(ctx, player, db_obj)
    await commands_recent(ctx, player, update_bool)


@bot.command(aliases=['compare'])
async def c(ctx, player: str = None):
    db_obj = Database()
    player, null = get_osu_username_from_param(ctx, player, db_obj)
    await commands_compare(ctx, player, bot)


@bot.command()
async def osutop(ctx, player: str = None, command_mode: str = None, play_number: int = 0):
    db_obj = Database()
    param_player = player # i need untouched player in this func
    if player == None or player == 'p' or player == 'r':
        discord_id = ctx.message.author.id
        player = db_obj.select_players_by_id(discord_id)
        update_bool = True
    elif len(player) > 20:
        discord_id = int(player.strip('<@!>'))
        player = db_obj.select_players_by_id(discord_id)
    else:
        player = {
            "osu_username" : player
        }
    # command_modes: 'p' = specific_play, 'r' = latest_topplays, None= osu_top
    if param_player == 'p': # if first parameter are 'p' it means parameters are shifted ex: normal usage= >osutop osu_username 'p' 55 db_user usage= >osutop 'p' 55
        play_number = int(command_mode) # shifting parameters
        command_mode = 'p'              # shifting parameters

    # i dont need same shifting on mode 'r' cause theres no another parameter in mode 'r'

    if command_mode == 'p':
        await commands_osutop_p(ctx, player, play_number)
    elif param_player == 'r' or command_mode == 'r':
        await commands_osutop_r(ctx, player)
    else:
        await commands_osutop(ctx, player)


@bot.command(aliases=['mapdata'])
async def map(ctx, beatmap_id: str = None, mods: str = 'No Mod'):
    if beatmap_id != None and beatmap_id.isnumeric() == False: # param shifting again see L#131 if confused
        mods = beatmap_id
        beatmap_id = None
    await commands_map(ctx, beatmap_id, mods)


@bot.command(aliases=['newtopplay'])
async def ntp(ctx, player: str = None, *pp_tuple):
    db_obj = Database()
    if player.isnumeric(): # param shifting
        discord_id = ctx.message.author.id
        pp_tuple += (player,)
        player = db_obj.select_players_by_id(discord_id)
    elif len(player) > 20: # not shifting thats mention
        discord_id = int(player.strip('<@!>'))
        player = db_obj.select_players_by_id(discord_id)
    else:
        player = {
            "osu_username" : player
        }

    await commands_ntp(ctx, player, pp_tuple)


@bot.command(aliases=['bonuspp'])
async def bpp(ctx, player: str = None):
    db_obj = Database()
    player, null = get_osu_username_from_param(ctx, player, db_obj)
    await commands_bpp(ctx, player)


@bot.command()
async def acc(ctx, count50, count100, mod:str = 'No Mod'):
    await commands_acc(ctx, count50, count100, mod)


@bot.command()
async def leaderboards(ctx):
    db_obj = Database()
    await commands_leaderboards(ctx, db_obj)


@bot.command()
async def link(ctx, osu_username: str = None):
    db_obj = Database()
    await commands_link(ctx, osu_username, db_obj)

@bot.command()
async def unlink(ctx):
    db_obj = Database()
    await commands_unlink(ctx, db_obj)

@bot.command()
async def help(ctx):
    await ctx.send(file=File(r"my_files\help.png"))


@bot.command()
async def aliases(ctx):
    await ctx.send(file=File(r"my_files\aliases.png"))


@bot.command(aliases=['global'])
async def g(ctx, mods='No Mod'):
    await commands_global(ctx, mods)


@bot.command(aliases=['compareserver'])
async def cs(ctx):
    db_obj = Database()
    await commands_compare_server(ctx, db_obj)

@bot.command()
async def roll(ctx, num=""):
    await commands_roll(ctx, num)


@bot.command()
@commands.is_owner()
async def talkmyboi(ctx, channel_id=526881587682344982, *message):
    channel = bot.get_channel(int(channel_id))
    output = ""
    for word in message:
        output += word + " "
    await channel.send(output)


load_dotenv(find_dotenv())
bot.run(os.getenv('BOT_TOKEN'))
