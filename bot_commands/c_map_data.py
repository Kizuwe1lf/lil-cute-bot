from bot_commands.c_main import stuff
from datetime import *
from scripts import *
import discord
import calendar


def get_len(seconds):
    minutes = int(seconds / 60)
    seconds = seconds - minutes * 60
    if seconds < 10:
        seconds = f"0{seconds}"
    return [minutes, seconds]


def get_beatmap_status(beatmap_status):
    if beatmap_status == 4: return "Loved"
    if beatmap_status == 3: return "Qualified"
    if beatmap_status == 2: return "Approved"
    if beatmap_status == 1: return "Ranked"
    if beatmap_status == 0: return "Pending"
    if beatmap_status == -1: return "Work in Progress"
    if beatmap_status == -2: return "Graveyard"


def spot_beatmap(guild_id, beatmap_id: str = None):
    if beatmap_id == None:
        beatmap_id = stuff.get_beatmap_id(guild_id)
        if not beatmap_id: return f"Theres no ~~beatmap_id~~ in cache"
    else:
        beatmap_id = beatmap_id.split("/")
        beatmap_id = beatmap_id[-1]
    beatmap = Beatmaps(beatmap_id)
    beatmap_data = beatmap.get_beatmap_data()
    beatmap_with_dt = Beatmaps(beatmap_id, 64)
    get_beatmaps = stuff.get_beatmaps(beatmap_id, guild_id)
    get_user = stuff.get_user(get_beatmaps[0]['creator'])
    r_g_b = download_thumbnails(get_beatmaps[0]['beatmapset_id'])
    e = discord.Embed(color=discord.colour.Colour.from_rgb(r_g_b[0], r_g_b[1], r_g_b[2]))
    if not get_user:
        e.set_author(name=f"Beatmap by {get_beatmaps[0]['creator']}")
    else:
        avatar_url = f"http://s.ppy.sh/a/{get_user[0]['user_id']}"
        profile_url = f"https://osu.ppy.sh/u/{get_user[0]['user_id']}"
        e.set_author(name=f"Beatmap by {get_user[0]['username']}", url=profile_url, icon_url=avatar_url)

    hit_len = get_len(int(get_beatmaps[0]['hit_length']))
    total_len = get_len(int(get_beatmaps[0]['total_length']))
    objectz = [int(get_beatmaps[0]['count_normal']), int(get_beatmaps[0]['count_slider']), int(get_beatmaps[0]['count_spinner']), ]
    obj = objectz[0] + objectz[1] + objectz[2]
    dt_accs = beatmap_with_dt.get_accuracy_pps()
    nomod_accs = beatmap.get_accuracy_pps()

    info = ""
    info += f"**[{get_beatmaps[0]['artist']} - {get_beatmaps[0]['title'].replace('*', ' ')} \n [{get_beatmaps[0]['version']}]]"
    info += f"(https://osu.ppy.sh/beatmapsets/{get_beatmaps[0]['beatmapset_id']}#osu/{get_beatmaps[0]['beatmap_id']})**\n \n"
    info += f"**Length:** `{total_len[0]}:{total_len[1]}` (`{hit_len[0]}:{hit_len[1]}`) **BPM:** `{get_beatmaps[0]['bpm']}` **Objects:** `{obj}`\n \n"
    info += f"**Circles:** `{objectz[0]}` **Sliders:** `{objectz[1]}` **Spinners:** `{objectz[2]}`\n"
    info += f"**CS:** `{beatmap_data[0]}` **AR:** `{beatmap_data[1]}` **OD:** `{beatmap_data[2]}` **HP:** `{beatmap_data[3]}` **SR:** `{beatmap.get_stars()}` (`{beatmap_with_dt.get_stars()}` DT) **MaxCombo:** `{get_beatmaps[0]['max_combo']}`\n \n"
    info += f"**Performance Points NoMod-DT** \n"
    info += f"`NM` 95%: {nomod_accs[0]}pp | 99%: {nomod_accs[2]}pp | 100%: {nomod_accs[3]}pp\n"
    info += f"`DT` 95%: {dt_accs[0]}pp | 99%: {dt_accs[2]}pp | 100%: {dt_accs[3]}pp"

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
    return e
