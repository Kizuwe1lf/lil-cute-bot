from bot_commands.c_main import stuff
import discord
import random
from scripts import *


async def commands_osu(ctx, player):
    if player == None:
        await ctx.send('User Not Linked')
        return 0

    osu_username = player['osu_username']
    get_user = stuff.get_user(osu_username) # request

    if not get_user:
        await ctx.send(f"~~{osu_username}~~ **was not found.**")
        return 0

    flag_url = f"https://osu.ppy.sh/images/flags/{get_user[0]['country']}.png"
    avatar_url = f"https://a.ppy.sh/{get_user[0]['user_id']}?{random.randint(100000, 999999)}"
    profile_url = f"https://osu.ppy.sh/u/{get_user[0]['user_id']}"
    e = discord.Embed(colour=ctx.message.author.colour)
    e.set_author(name=f"osu! Profile for Random Filthy Weeb", url=profile_url, icon_url=flag_url)
    e.set_thumbnail(url=avatar_url)
    info = ""
    info += f"**▸ Username:**   {(get_user[0]['username'])}\n"
    info += f"**▸ Rank:** #{get_user[0]['pp_rank']} [{get_user[0]['country']}#{get_user[0]['pp_country_rank']}]\n"
    info += f"**▸ Total PP:** {float(get_user[0]['pp_raw']):0.2f}\n"
    info += f"**▸ Hit Accuracy:** {float(get_user[0]['accuracy']):0.2f}%\n"
    info += f"**▸ Playcount:** {get_user[0]['playcount']}\n"
    info += f"**▸ Hours Played:** {get_total_hours_played(get_user[0]['total_seconds_played'])}"
    e.description = info
    await send_embed(ctx, e)
