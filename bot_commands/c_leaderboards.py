import discord
from scripts import *

async def commands_leaderboards(ctx, db_obj):
    members = db_obj.select_players_by_server(ctx.guild.id)
    members = sorted(members, key=lambda x:x['pp_raw'], reverse=True)

    description = ""
    multi_link_count = 0
    i = 0
    while i < len(members) and i < 20:
        if i >= 1 and members[i]['osu_user_id'] == members[i-1]['osu_user_id']:
            multi_link_count += 1
        else:
            profile_url = f"(https://osu.ppy.sh/u/{members[i]['osu_user_id']})"
            osu_user = f"[{members[i]['osu_username']}]"
            description += f"**{(i + 1)-multi_link_count}.** {osu_user}{profile_url} **{round_func(members[i]['pp_raw'])}pp** #{members[i]['pp_rank']} {members[i]['country']}#{members[i]['pp_country_rank']}\n"
        i += 1

    e = discord.Embed(colour=ctx.message.author.colour)
    e.set_author(name=f"osu! Ranking for {ctx.guild.name}")
    e.set_thumbnail(url=ctx.guild.icon_url)
    e.description = description
    e.set_footer(text=f"{len(members)-multi_link_count} players linked in {ctx.guild.name}")
    await send_embed(ctx, e)
