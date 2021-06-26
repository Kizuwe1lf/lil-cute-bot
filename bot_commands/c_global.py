from write_to_image import *


async def commands_global(ctx, request_obj, mods):
    beatmap_id = request_obj.get_beatmap_id(ctx.channel.id)
    if not beatmap_id:
        await ctx.send(f"Theres no ~~beatmap_id~~ in cache")
        return 0
    if check_if_mods_are_invalid(mods) == 0:
        await ctx.send('Invalid Mods')
        return 0
    mods_int = ""
    if mods != 'No Mod':
        mods_int = f"&mods={mod_to_num(mods)}"
    scores = request_obj.get_global(beatmap_id, mods_int)
    get_beatmaps = request_obj.get_beatmaps(beatmap_id, ctx.channel.id)
    await write_to_image(ctx, scores, get_beatmaps, 'global')
