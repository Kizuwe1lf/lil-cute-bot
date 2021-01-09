from bot_commands.c_main import stuff
from scripts import *


def get_acc(acc, guild_id, mod=0):
    beatmap_id = stuff.get_beatmap_id(guild_id)
    if not beatmap_id: return f"Theres no ~~beatmap_id~~ in cache"
    if mod != 0: mod = mod_to_num(str(mod))
    beatmap = Beatmaps(beatmap_id, mod)
    mod = num_to_mod(mod)
    pp = beatmap.get_if_fc_pp(acc)
    x = f"| {float(acc):0.2f}% +{mod} {pp}"
    return x.replace('IF', '')