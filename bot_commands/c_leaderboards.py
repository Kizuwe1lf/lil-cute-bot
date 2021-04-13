import discord
from database import *



def get_leaderboards(ctx):
    db_object = Database()
    discord_id_list = []
    description = ""


    for member in ctx.guild.members:
        discord_id_list.append(member.id)

    member_list = db_object.multiple_select_from_database(discord_id_list)
    multi_link_count = 0
    member_list.sort(key=lambda x:x[4], reverse=true)

    i = 0
    while i+multi_link_count < len(member_list) and i+multi_link_count < 21:
        if i >= 1 and member_list[i][2] == member_list[i-1][2]:
            multi_link_count += 1
        else:
            profile_url = f"(https://osu.ppy.sh/u/{member_list[i][2]})"
            osu_user = f"[{member_list[i][1]}]"
            description += f"**{(i + 1)-multi_link_count}.** {osu_user}{profile_url} **{member_list[i][4]}pp** #{member_list[i][3]} {member_list[i][6]}#{member_list[i][5]}\n"
        i += 1

    e = discord.Embed(colour=ctx.message.author.colour)
    e.set_author(name=f"osu! Ranking for {ctx.guild.name}")
    e.set_thumbnail(url=ctx.guild.icon_url)
    e.description = description
    e.set_footer(text=f"{len(member_list)-multi_link_count} player linked in {ctx.guild.name}")
    return e
