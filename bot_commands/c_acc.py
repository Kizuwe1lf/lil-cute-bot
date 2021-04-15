from bot_commands.c_main import stuff
from scripts import *


async def commands_acc(ctx, count50, count100, mods:str = 'No Mod'):
    beatmap_id = stuff.get_beatmap_id(ctx.channel.id)
    mods_list = get_mod_list_from_mods_string(mods)

    if not beatmap_id:
        await ctx.send(f"Theres no ~~beatmap_id~~ in cache")
        return 0
    if check_if_mods_are_invalid(mods_list) == 0:
        await ctx.send('Invalid Mods')
        return 0
    if count50.isnumeric() == False or count100.isnumeric() == False:
        await ctx.send("Invalid Count50&Count100")
        return 0

    count = [0, int(count50), int(count100)]
    if_fc_pp_resp = get_if_fc_pp(beatmap_id, mods_list, count)
    await ctx.send(f"{if_fc_pp_resp['accuracy']}% +{mods} FC: **{if_fc_pp_resp['pp']}**pp")
