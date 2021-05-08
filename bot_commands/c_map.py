from datetime import *
from scripts import *
import discord
import calendar


def get_len_and_bpm(seconds, bpm, mod):
    if mod == 'DT':
        seconds /= 1.5 # dt formula it increases the speed of beatmaps by 150%
        bpm *= 1.5
    elif mod == 'HT':
        seconds /= 0.75 # ht formula it decreases the speed of beatmaps by 75%
        bpm /= 0.75

    minutes = int(seconds / 60)
    seconds = round(seconds - minutes * 60)
    if seconds < 10:
        seconds = f"0{seconds}"
    return [minutes, seconds, round_func(bpm)]


def get_beatmap_status(beatmap_status):
    if beatmap_status == 4: return "Loved"
    if beatmap_status == 3: return "Qualified"
    if beatmap_status == 2: return "Approved"
    if beatmap_status == 1: return "Ranked"
    if beatmap_status == 0: return "Pending"
    if beatmap_status == -1: return "Work in Progress"
    if beatmap_status == -2: return "Graveyard"


async def commands_map(ctx, request_obj, beatmap_id, mods: list = ['No Mod']):
    if beatmap_id == None:
        beatmap_id = request_obj.get_beatmap_id(ctx.channel.id)
    if not beatmap_id:
        await ctx.send(f"Theres no ~~beatmap_id~~ in cache")
        return 0

    get_beatmaps = request_obj.get_beatmaps(beatmap_id, ctx.channel.id)
    get_user = request_obj.get_user(get_beatmaps[0]['creator'])
    r_g_b = get_avg_colour_from_cover(get_beatmaps[0]['beatmapset_id'])
    e = discord.Embed(color=discord.colour.Colour.from_rgb(r_g_b[0], r_g_b[1], r_g_b[2]))
    if not get_user:
        e.set_author(name=f"Beatmap by {get_beatmaps[0]['creator']}")
    else:
        avatar_url = f"http://s.ppy.sh/a/{get_user[0]['user_id']}"
        profile_url = f"https://osu.ppy.sh/u/{get_user[0]['user_id']}"
        e.set_author(name=f"Beatmap by {get_user[0]['username']}", url=profile_url, icon_url=avatar_url)

    mods_list = get_mod_list_from_mods_string(mods)

    if check_if_mods_are_invalid(mods_list) == 0:
        return 'Invalid Mods'

    objectz = [int(get_beatmaps[0]['count_normal']), int(get_beatmaps[0]['count_slider']), int(get_beatmaps[0]['count_spinner']), ]
    obj = objectz[0] + objectz[1] + objectz[2]


    star_rating = get_difficulty(beatmap_id, mods_list)
    map_data = get_beatmap_data(beatmap_id, mods_list)
    mods_string = ''.join(mods_list)

    if 'DT' in mods_list or 'NC' in mods_list:
        mod_formula = 'DT'
    elif 'HT' in mods_list:
        mod_formula = 'HT'
    else:
        mod_formula = 'Wee'

    bpm = float(get_beatmaps[0]['bpm'])
    hit_len = get_len_and_bpm(int(get_beatmaps[0]['hit_length']), bpm, mod_formula)
    total_len = get_len_and_bpm(int(get_beatmaps[0]['total_length']), bpm, mod_formula)

    info = ""
    info += f"**[{get_beatmaps[0]['artist']} - {get_beatmaps[0]['title'].replace('*', ' ')} \n [{get_beatmaps[0]['version']}]]"
    info += f"(https://osu.ppy.sh/beatmapsets/{get_beatmaps[0]['beatmapset_id']}#osu/{get_beatmaps[0]['beatmap_id']})**\n \n"
    info += f"**Mods** +{mods_string}\n\n"
    info += f"**Length:** `{total_len[0]}:{total_len[1]}` (`{hit_len[0]}:{hit_len[1]}`) **BPM:** `{hit_len[2]}` **MaxCombo:** `{get_beatmaps[0]['max_combo']}`\n"
    info += f"**Objects:**    | **Circles:** `{objectz[0]}` **Sliders:** `{objectz[1]}` **Spinners:** `{objectz[2]}` **Total** `{obj}`\n"
    info += f"**StarRatings** | **Aim** `{map_data['aimsr']}` **Speed** `{map_data['speedsr']}` **Total** `{map_data['sr']}`\n"

    footer_text = ""
    footer_text += f"{get_beatmap_status(int(get_beatmaps[0]['approved']))} | {get_beatmaps[0]['favourite_count']} ❤"

    if get_beatmaps[0]['approved_date'] is not None:
        a = (datetime.strptime(get_beatmaps[0]['approved_date'], '%Y-%m-%d %H:%M:%S').date())
        footer_text += f" | Approved {calendar.month_name[a.month]} {a.day} {a.year}"
    elif get_beatmaps[0]['last_update'] is not None:
        a = (datetime.strptime(get_beatmaps[0]['last_update'], '%Y-%m-%d %H:%M:%S').date())
        footer_text += f" | Last Updated {calendar.month_name[a.month]} {a.day} {a.year}"
    try:
        e.set_image(url=f"https://assets.ppy.sh/beatmaps/{get_beatmaps[0]['beatmapset_id']}/covers/cover.jpg")
    except:
        pass
    e.set_footer(text=footer_text)
    e.description = info
    await send_embed(ctx, e)
