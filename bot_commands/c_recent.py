from bot_commands.c_main import stuff
import discord
from datetime import *
from scripts import *
import random
from get_user import *


def get_recent1(osu_user, guild_id, my_update_bool, discord_id):
    get_user = stuff.get_user(osu_user)
    get_recent = stuff.get_user_recent(osu_user)
    try_counter = 1
    

    if not get_user:   return f"~~{osu_user}~~ **was not found.**"
    if not get_recent:
        return f"~~{get_user[0]['username']}~~ **did not submit anything recently.**"
    else:
        if my_update_bool:
            update_user(discord_id, get_user)
        for x in range(len(get_recent)-1):
            if get_recent[0]['beatmap_id'] == get_recent[x + 1]['beatmap_id'] and get_recent[0]['enabled_mods'] == get_recent[x + 1]['enabled_mods']:
                try_counter += 1
            else:
                break
        beatmap = Beatmaps(get_recent[0]['beatmap_id'], int(get_recent[0]['enabled_mods']))
        get_beatmaps = stuff.get_beatmaps(get_recent[0]['beatmap_id'], guild_id)
        r_g_b = download_thumbnails(get_beatmaps[0]['beatmapset_id'])
        count = [get_recent[0]['countmiss'], get_recent[0]['count50'], get_recent[0]['count100'], get_recent[0]['count300']]
        get_scores = stuff.get_global(get_recent[0]['beatmap_id'], "")
        rank_text = ""
        for x in range(len(get_scores)):
            if get_scores[x]['score'] == get_recent[0]['score'] and get_scores[x]['user_id'] == get_recent[0]['user_id']:
                rank_text = f"| Global**#{x+1}**"
        total_hits = 0
        for items in count:
            total_hits += int(items)
        pp_play = ""
        if get_recent[0]['rank'] != 'F':
            pp_play = beatmap.get_pp(int(get_recent[0]['maxcombo']), *count)
        score = get_score(get_recent[0]['score'])
        fc_pp = ""
        player_combo_text = "x"
        player_combo_text += get_recent[0]['maxcombo']
        if int(get_beatmaps[0]['max_combo']) - int(get_recent[0]['maxcombo']) > 6 or int(count[0]) > 0 or get_recent[0]['rank'] == 'F':
            fc_pp = beatmap.get_if_fc_pp(no_choke_acc(*count))
        if get_recent[0]['perfect'] == "0":
            player_combo_text = f"**{player_combo_text}**"

        e = discord.Embed(color=discord.colour.Colour.from_rgb(r_g_b[0], r_g_b[1], r_g_b[2]))
        flag_url = f"https://osu.ppy.sh/images/flags/{get_user[0]['country']}.png"
        e.set_author(name=f"{get_user[0]['username']}: {get_user[0]['pp_raw']}pp\n(#{get_user[0]['pp_rank']} {get_user[0]['country']}{get_user[0]['pp_country_rank']})", url=f"https://osu.ppy.sh/u/{get_user[0]['user_id']}", icon_url=flag_url)
        try:
            e.set_image(url=f"https://assets.ppy.sh/beatmaps/{get_beatmaps[0]['beatmapset_id']}/covers/cover.jpg")
        except:
            pass
        avatar_url = f"https://a.ppy.sh/{get_user[0]['user_id']}?{random.randint(100000, 999999)}"
        e.set_thumbnail(url=avatar_url)

        info = f"**[{get_beatmaps[0]['title'].replace('*', ' ')} [{get_beatmaps[0]['version']}]](https://osu.ppy.sh/beatmapsets/{get_beatmaps[0]['beatmapset_id']}#osu/{get_beatmaps[0]['beatmap_id']})**\n"
        info += f"▸ **[{beatmap.get_stars()}★]** +{num_to_mod(get_recent[0]['enabled_mods'])} | {score} **-** {get_rank_emote(get_recent[0]['rank'])}\n"
        info += f"▸  {pp_play} {fc_pp} ** {player_combo_text}/{get_beatmaps[0]['max_combo']}**\n"
        info += f"▸ {acc_calculator(*count):0.2f}% | {count[2]}x{get_onehundred_emote()} | {count[1]}x{get_fifty_emote()} | {count[0]}{get_miss_emote()}\n"
        info += f"▸ Try **#{try_counter}** | {time_ago(datetime.strptime(get_recent[0]['date'], '%Y-%m-%d %H:%M:%S'), datetime.utcnow())} {rank_text}\n"
        if get_recent[0]['rank'] == 'F': info += f"▸ Map Completion: {beatmap.get_mapcompletion(total_hits)}%\n"
        nomod_accs = beatmap.get_accuracy_pps()
        footer_text = f"95%: {nomod_accs[0]}pp | 98%: {nomod_accs[1]}pp"
        footer_text += f" | 99%: {nomod_accs[2]}pp | 100%: {nomod_accs[3]}pp"
        e.set_footer(text=footer_text)
        e.description = info
        return e
