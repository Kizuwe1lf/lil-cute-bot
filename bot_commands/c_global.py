from bot_commands.c_main import stuff
from write_to_image import *


async def commands_global(ctx, mods):
    beatmap_id = stuff.get_beatmap_id(ctx.channel.id)

    if not beatmap_id:
        await ctx.send(f"Theres no ~~beatmap_id~~ in cache")
        return 0
    if check_if_mods_are_invalid(mods) == 0:
        await ctx.send('Invalid Mods')
        return 0

    mods_int = mod_to_num(mods)
    scores = stuff.get_global(beatmap_id, mods_int)
    get_beatmaps = stuff.get_beatmaps(beatmap_id, ctx.channel.id)
    await write_to_image(ctx, scores, get_beatmaps)
