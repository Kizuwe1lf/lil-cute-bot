from write_to_image import *
from database import *


async def commands_compare_server(ctx, request_obj, db_obj):
    beatmap_id = request_obj.get_beatmap_id(ctx.channel.id)
    if not beatmap_id:
        await ctx.send(f"Theres no ~~beatmap_id~~ in cache")
        return 0

    members = db_obj.select_players_by_server(ctx.guild.id)
    scores = []

    for member in members:
        get_scores = request_obj.get_scores(member['osu_user_id'], beatmap_id, ctx.channel.id)
        if get_scores:
            scores.append(get_scores[0])

    scores = sorted(scores, key=lambda x:int(x['score']), reverse= True)
    get_beatmaps = request_obj.get_beatmaps(beatmap_id, ctx.channel.id)
    await write_to_image(ctx, scores, get_beatmaps)
