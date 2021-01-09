from bot_commands.c_main import stuff
from write_to_image import *



def get_global_image(guild_id, mods):
    beatmap_id = stuff.get_beatmap_id(guild_id)
    if not beatmap_id: return f"Theres no ~~beatmap_id~~ in cache"
    if mods == "":
        pass
    else:
        mods = mod_to_num(mods)
    scores = stuff.get_global(beatmap_id, mods)
    get_beatmaps = stuff.get_beatmaps(beatmap_id, guild_id)
    return write_to_image(scores, get_beatmaps)
    