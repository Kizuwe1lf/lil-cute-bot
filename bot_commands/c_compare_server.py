from bot_commands.c_main import stuff
from write_to_image import *
from database import *


def get_compare_server_image(ctx):
    guild_id = ctx.channel.id
    beatmap_id = stuff.get_beatmap_id(guild_id)
    if not beatmap_id: return f"Theres no ~~beatmap_id~~ in cache"


    db_object = Database()
    discord_id_list = []

    for member in ctx.guild.members:
        discord_id_list.append(member.id)

    member_list = db_object.multiple_select_from_database(discord_id_list)

    data = []

    for member in member_list:
        get_scores = stuff.get_scores(member[1], beatmap_id, guild_id)
        if get_scores:
            data.append(get_scores[0])
    data.sort(key=lambda x:int(x['score']), reverse= True)
    get_beatmaps = stuff.get_beatmaps(beatmap_id, guild_id)
    return write_to_image(data, get_beatmaps)
