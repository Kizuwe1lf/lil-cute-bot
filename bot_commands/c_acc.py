from scripts import *


async def commands_acc(ctx, request_obj, count100, count50, mods:str = 'No Mod'):
    beatmap_id = request_obj.get_beatmap_id(ctx.channel.id)
    mods_list = get_mod_list_from_mods_string(mods)
    mods_string = ''.join(mods_list)

    if not beatmap_id:
        await ctx.send(f"Theres no ~~beatmap_id~~ in cache")
    elif check_if_mods_are_invalid(mods_list) == 0:
        await ctx.send('Invalid Mods')
    elif count50.isnumeric() == False or count100.isnumeric() == False:
        await ctx.send("Invalid Count50&Count100")
    else:
        count = [0, int(count50), int(count100)]
        if_fc_pp_resp = get_if_fc_pp(beatmap_id, mods_list, count)
        await ctx.send(f"{if_fc_pp_resp['accuracy']}% +{mods_string} FC: **{if_fc_pp_resp['pp']}**pp")
