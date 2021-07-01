import discord
from scripts import *

async def commands_global_leaderboards(ctx, db_obj, bot_avatar_url, bot_user_name):
    everyone = db_obj.select_everyone()
    i = 0
    description = []
    for member in everyone:
        i += 1
        profile_url = f"(https://osu.ppy.sh/u/{member['osu_user_id']})"
        osu_user = f"[{member['osu_username']}]"
        output = f"**{(i)}.** {osu_user}{profile_url} \
                   **{round_func(member['pp_raw'])}pp** \
                   #{member['pp_rank']} {member['country']}\
                   #{member['pp_country_rank']}"
        description.append(output)

    e = discord.Embed(colour=ctx.message.author.colour)
    e.set_author(name=f"osu! Global Ranking for {bot_user_name}")
    e.set_thumbnail(url=bot_avatar_url)
    e.description = '\n'.join(description[:20])
    e.set_footer(text=f"{i} players linked with {bot_user_name}")
    await send_embed(ctx, e)
