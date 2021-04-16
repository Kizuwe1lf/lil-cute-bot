import asyncio
from downloader import *
import pyttanko as osu
import os
from subprocess import Popen, PIPE
import json
import discord


def get_map_completion(beatmap_id, total_hits):
    osu_map_path =  get_beatmap_path(beatmap_id)

    p = osu.parser() #
    with open(os.path.join(osu_map_path), "r", encoding="utf-8") as f:
        bmap = p.map(f)

        hitobj = []
        if total_hits == 0:
            total_hits = len(bmap.hitobjects)
        numobj = total_hits - 1
        num = len(bmap.hitobjects)
        for objects in bmap.hitobjects:
            hitobj.append(objects.time)
        timing = int(hitobj[num - 1]) - int(hitobj[0])
        point = int(hitobj[numobj]) - int(hitobj[0])
        map_completion = (point / timing) * 100
    return round_func(map_completion)

def calc(param):
    calc_path = ["my_files/pp_calculator/PerformanceCalculator.exe"]
    process = Popen(calc_path + param, stdout=PIPE)
    output = process.communicate()[0]
    return json.loads(output)

def get_difficulty(beatmap_id, mods_list):
    bmap_path = get_beatmap_path(beatmap_id)
    param = ['difficulty', bmap_path]
    param = add_mods_to_param_for_calc(param, mods_list)
    return calc(param)['sr']

def get_pp(beatmap_id, mods_list, maxcombo, count): # count has [miss, 50, 100, 300] counts
    bmap_path = get_beatmap_path(beatmap_id)
    param = ['simulate', 'osu', bmap_path, f'-c {maxcombo}', f'-X {count[0]}', f'-M {count[1]}', f'-G {count[2]}']
    param = add_mods_to_param_for_calc(param, mods_list)
    return calc(param)

def get_if_fc_pp(beatmap_id, mods_list, count):
    bmap_path = get_beatmap_path(beatmap_id)
    param = ['simulate', 'osu', bmap_path, f'-M {count[1]}', f'-G {count[2]}'] #excluding misses
    param = add_mods_to_param_for_calc(param, mods_list)
    return calc(param)

def get_beatmap_data(beatmap_id, mods_list):
    bmap_path = get_beatmap_path(beatmap_id)
    param = ['difficulty', bmap_path]
    param = add_mods_to_param_for_calc(param, mods_list)
    return calc(param)

def get_if_fc_pp_text(pp):
    return f"IF FC : **{pp}**pp |"

def get_pp_text(pp):
    return f"**{pp}**pp |"

def calc_accuracy(x, y, z, c): # x,y,z,c  miss 50 100 300
    total_score = float(y)
    total_score += float(z)
    total_score += float(c)
    total_score += float(x)
    total_score *= 300
    user_score = float(y) * 50
    user_score += float(z) * 100
    user_score += float(c) * 300
    return round_func(float(user_score) * 100 / float(total_score))

def num_to_mod_list(number):
    mod_list = []
    number = int(number)
    if number == 0:
        mod_list.append('No Mod')
        return mod_list
    if   number & 1 << 0:   mod_list.append('NF')
    if   number & 1 << 1:   mod_list.append('EZ')
    if   number & 1 << 2:   mod_list.append('TD')
    if   number & 1 << 3:   mod_list.append('HD')
    if   number & 1 << 4:   mod_list.append('HR')
    if   number & 1 << 5:   mod_list.append('SD')
    if   number & 1 << 9:
        mod_list.append('NC')
    elif number & 1 << 6:
        mod_list.append('DT')
    if   number & 1 << 7:   mod_list.append('RX')
    if   number & 1 << 8:   mod_list.append('HT')
    if   number & 1 << 10:  mod_list.append('FL')
    if   number & 1 << 12:  mod_list.append('SO')
    if   number & 1 << 14:  mod_list.append('PF')
    if   number & 1 << 20:  mod_list.append('FI')
    if   number & 1 << 29:  mod_list.append('v2')
    return mod_list

def mod_to_num(mods: str):
    mods = mods.upper()
    total = 0
    if   'No Mod' in mods: return total
    if   'NF' in mods:    total += 1 << 0
    if   'EZ' in mods:    total += 1 << 1
    if   'TD' in mods:    total += 1 << 2
    if   'HD' in mods:    total += 1 << 3
    if   'HR' in mods:    total += 1 << 4
    if   'SD' in mods:    total += 1 << 5
    if   'NC' in mods:
        total += (( 1 << 9 ) + ( 1 << 6 ))
    elif 'DT' in mods:
        total += 1 << 6
    if   'RX' in mods:    total += 1 << 7
    if   'HT' in mods:    total += 1 << 8
    if   'FL' in mods:    total += 1 << 10
    if   'SO' in mods:    total += 1 << 12
    if   'PF' in mods:    total += 1 << 14
    if   'FI' in mods:    total += 1 << 20
    if   'v2' in mods:    total += 1 << 29

    return int(total)


def num_to_num_diff_inc_mods_only(number): # weee i dont use that
    total = 0
    if   number & 1 << 4:
        total += 1 << 4
    if   number & 1 << 1:
        total += 1 << 1
    if  number & 1 << 9:
        total += 1 << 6
    elif number & 1 << 6:
        total += 1 << 6
    if number & 1 << 8:
        total += 1 << 8

    return total




def get_fifty_emote():
    return f"<:50_Emote:649799152519086082>"


def get_onehundred_emote():
    return f"<:100_Emote:649794377954230283>"


def get_miss_emote():
    return f"<:Miss_Emote:649801261046038528>"


def get_rank_emote(rank):
    if rank == "A":
        return "<:A_Emote:649752233226928131>"
    if rank == "B":
        return "<:B_Emote:649752243259703317>"
    if rank == "C":
        return "<:C_Emote:649752253883744265>"
    if rank == "D":
        return "<:D_Emote:649752265095380993>"
    if rank == "XH":  # SS hidden
        return "<:SSH_Emote:649752313677873184>"
    if rank == "SH":  # S Hidden
        return "<:SH_Emote:649752294665093140>"
    if rank == "X":  # SS
        return "<:SS_Emote:649752304357998632>"
    if rank == "S":
        return "<:S_Emote:649752285613785121>"
    if rank == "F":
        return "<:F_Emote:649752275694125056>"

    return rank

def time_ago(play_time, base_time):
    totalseconds = (base_time - play_time).total_seconds()
    total_minutes = totalseconds / 60
    total_hours = total_minutes / 60
    total_days = total_hours / 24
    total_months = total_days / 30
    total_years = total_months / 12

    if totalseconds <= 30:
        return "Submitted **Just Now**"
    elif totalseconds < 60:
        return f"**{int(totalseconds)} seconds** ago"
    elif total_minutes < 60:
        return f"**{int(total_minutes)} minutes** ago"
    elif total_hours < 24:
        return f"**{int(total_hours)} hours** ago"
    elif total_days < 30:
        return f"**{int(total_days)} days** ago"
    elif total_months < 12:
        if total_days - int(total_months) * 30 >= 5:
            return f"**{int(total_months)} months {int(total_days - int(total_months) * 30)} days** ago"
        else:
            return f"**{int(total_months)} months** ago"
    else:
        if total_months - int(total_years) * 12 >= 1:
            return f"**{int(total_years)} years {int(total_months - int(total_years) * 12)} months** ago"
        else:
            return f"**{int(total_years)} years** ago"

def get_score(score):
    return '{:,}'.format(int(score))


def get_total_hours_played(seconds):
    return int(round(int(seconds) / 60 / 60))

def check_if_mods_are_invalid(mods): # works with str_mods and list_mods  ex: 'HDDTEZ' or ['HD', 'DT', 'EZ']
    if 'No Mod' in mods and mods != 'No Mod' and len(mods) > 1:
        return 0
    if 'DT' in mods or 'NC' in mods:
        if 'HT' in mods:  # DT or NC and HT
            return 0
        elif 'DT' in mods and 'NC' in mods: # DT and NC
            return 0
    if 'HR' in mods and 'EZ' in mods: # HR and EZ
        return 0
    if 'SD' in mods or 'PF' in mods:
        if 'SD' in mods and 'PF' in mods: # SD and PF
            return 0
        elif 'NF' in mods: # SD or PF and NF
            return 0

    return 1 # Poggers

def add_mods_to_param_for_calc(param, mods_list):
    if 'No Mod' not in mods_list:
        for mod in mods_list:
            param.append(f'-m {mod}')
    return param


def get_mod_list_from_mods_string(mods):
    available_mods = ['NF', 'EZ', 'TD', 'HD', 'HR', 'NC', 'DT', 'HT', 'FL', 'SO']
    mods_list = []
    while mods:
        if mods[:2].upper() in available_mods:
            mods_list.append(mods[:2].upper())
        mods = mods[2:]
    if mods_list == []:
        mods_list = ['No Mod']
    return mods_list


def round_func(val): # rounds with 2 dec ex: 3 = 3.00 ---- 3.5556 = 3.55
    return f"{float(val):0.2f}"

async def send_embed(ctx, e):
    await ctx.send(content=None, embed=e)

def get_osu_username_from_param(ctx, player, db_obj):
    update_bool = False
    if player == None:
        discord_id = ctx.message.author.id
        player = db_obj.select_players_by_id(discord_id)
        update_bool = True
    elif len(player) > 20:
        discord_id = int(player.strip('<@!>'))
        player = db_obj.select_players_by_id(discord_id)
    else:
        player = {
            "osu_username" : player
        }
    return player, update_bool

async def send_pages(ctx, e, info, total_pages, bot):
    cur_page = 1
    left = "<:slide_left:734860817584881674>"
    right = "<:slide_right:734860832642433164>"
    e.description = info[cur_page-1]
    e.set_footer(text=f"Pages {cur_page} out of {total_pages}")
    message = await ctx.send(embed=e)
    await message.add_reaction(right)

    def check(r, u):
        return u == ctx.message.author and str(r.message) == str(message) and (str(r.emoji) == left or str(r.emoji) == right)

    while True:
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
            if str(reaction.emoji) == right:
                await message.clear_reaction(right)
                await message.clear_reaction(left)
                cur_page += 1
                e.description = info[cur_page - 1]
                e.set_footer(text=f"Pages {cur_page} out of {total_pages}")
                await message.edit(embed=e)
                await message.add_reaction(left)
                if cur_page != total_pages:
                    await message.add_reaction(right)

            elif str(reaction.emoji) == left:
                await message.clear_reaction(right)
                await message.clear_reaction(left)
                cur_page -= 1
                e.description = info[cur_page - 1]
                e.set_footer(text=f"Pages {cur_page} out of {total_pages}")
                await message.edit(content=None, embed=e)
                if cur_page != 1:
                    await message.add_reaction(left)
                await message.add_reaction(right)
        except asyncio.TimeoutError:
            break
