from bot_commands.c_main import stuff
from scripts import *


def get_acc(counter50, counter100, guild_id, mods:str = 'No Mod'):
    try:
        beatmap_id = stuff.get_beatmap_id(guild_id)
        if not beatmap_id: return f"Theres no ~~beatmap_id~~ in cache"
        mods_list = get_mod_list_from_mods_string(mods)
        if check_if_mods_are_invalid(mods_list) == 0:
            return 'Invalid Mods'
        count = [0, count50, count100]
        pp = get_if_fc_pp(beatmap_id, mods_list, count)
        output = f"{round(acc, 2)}% +{mod} FC: **{pp}**pp"
        return output
    except:
        return 'Somethin went wrong'
