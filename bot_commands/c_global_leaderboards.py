import discord
from scripts import *

async def commands_global_leaderboards(ctx, db_obj, bot_avatar_url, bot_user_name):
    everyone = db_obj.select_everyone()
    everyone = sorted(everyone, key=lambda x:x['pp_raw'], reverse=True)

    description = ""
    multi_link_count = 0
    i = 0
    while i < len(everyone) and i < 21:
        if i >= 1 and everyone[i]['osu_user_id'] == everyone[i-1]['osu_user_id']:
            multi_link_count += 1
        else:
            profile_url = f"(https://osu.ppy.sh/u/{everyone[i]['osu_user_id']})"
            osu_user = f"[{everyone[i]['osu_username']}]"
            description += f"**{(i + 1)-multi_link_count}.** {osu_user}{profile_url} **{round_func(everyone[i]['pp_raw'])}pp** #{everyone[i]['pp_rank']} {everyone[i]['country']}#{everyone[i]['pp_country_rank']}\n"
        i += 1

    e = discord.Embed(colour=ctx.message.author.colour)
    e.set_author(name=f"osu! Global Ranking for {bot_user_name}")
    e.set_thumbnail(url=bot_avatar_url)
    e.description = description
    e.set_footer(text=f"{len(everyone)-multi_link_count} players linked with {bot_user_name}")
    await send_embed(ctx, e)
