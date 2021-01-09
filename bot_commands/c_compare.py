from bot_commands.c_main import stuff
import discord
from datetime import *
from scripts import *
import random


def compare(osu_user, guild_id):
    beatmap_id = stuff.get_beatmap_id(guild_id)
    get_user = stuff.get_user(osu_user)
    get_scores = stuff.get_scores(osu_user, beatmap_id, guild_id)
    if not beatmap_id: return f"Theres no ~~beatmap_id~~ in cache"
    if not get_user:  return f"~~{osu_user}~~ **was not found.**"
    if not get_scores: return f"~~{get_user[0]['username']}~~ **has no scores on the map.**"
    else:

        page_counter = 1
        page_description = []
        get_beatmaps = stuff.get_beatmaps(beatmap_id, guild_id)
        colors = download_thumbnails(get_beatmaps[0]['beatmapset_id'])
        flag_url = f"https://osu.ppy.sh/images/flags/{get_user[0]['country']}.png"
        e = discord.Embed(color=discord.colour.Colour.from_rgb(colors[0], colors[1], colors[2]))
        info = f"**[{get_beatmaps[0]['title'].replace('*', ' ')} [{get_beatmaps[0]['version']}]](https://osu.ppy.sh/beatmapsets/{get_beatmaps[0]['beatmapset_id']}#osu/{get_beatmaps[0]['beatmap_id']})**\n"
        e.set_author(name=f"Top plays on this map for {get_scores[0]['username']}\n{get_user[0]['pp_raw']}pp (#{get_user[0]['pp_rank']} {get_user[0]['country']}{get_user[0]['pp_country_rank']})", url=f"https://osu.ppy.sh/u/{get_user[0]['user_id']}", icon_url=flag_url)
        for x in range(0, len(get_scores)):
            if x == 3 or x == 6:
                page_description.append(info)
                info = f"**[{get_beatmaps[0]['title'].replace('*', ' ')} [{get_beatmaps[0]['version']}]](https://osu.ppy.sh/beatmapsets/{get_beatmaps[0]['beatmapset_id']}#osu/{get_beatmaps[0]['beatmap_id']})**\n"
                page_counter += 1
            beatmap = Beatmaps(get_beatmaps[0]['beatmap_id'], int(get_scores[x]['enabled_mods']))
            count = [get_scores[x]['countmiss'], get_scores[x]['count50'], get_scores[x]['count100'], get_scores[x]['count300']]
            score = get_score(get_scores[x]['score'])
            fc_pp = ""
            player_combo_text = "x"
            player_combo_text += get_scores[x]['maxcombo']
            if int(get_beatmaps[0]['max_combo']) - int(get_scores[x]['maxcombo']) > 6 or int(count[0]) > 0:
                fc_pp = beatmap.get_if_fc_pp(no_choke_acc(*count))
            if get_scores[x]['perfect'] == "0":
                player_combo_text = f"**{player_combo_text}**"
            if get_scores[x]['pp'] is not None:
                pp_text = f"**{float(get_scores[x]['pp']):0.0f}**pp"
            else:
                pp_text = beatmap.get_pp(int(get_scores[x]['maxcombo']), *count)
            info += f"▸ **[{beatmap.get_stars()}★]** +{num_to_mod(get_scores[x]['enabled_mods'])} | {score} **-** {get_rank_emote(get_scores[x]['rank'])} \n"
            info += f"▸ {pp_text} {fc_pp} ** {player_combo_text}/{get_beatmaps[0]['max_combo']}**\n"
            info += f"▸ {acc_calculator(*count):0.2f}% | {count[2]}x{get_onehundred_emote()} | {count[1]}x{get_fifty_emote()} | {count[0]}{get_miss_emote()}\n"
            info += f"▸ Score Set {time_ago(datetime.strptime(get_scores[x]['date'], '%Y-%m-%d %H:%M:%S'), datetime.utcnow())}\n \n"
        page_description.append(info)
        avatar_url = f"https://a.ppy.sh/{get_user[0]['user_id']}?{random.randint(100000, 999999)}"
        e.set_thumbnail(url=avatar_url)
        try:
            e.set_image(url=f"https://assets.ppy.sh/beatmaps/{get_beatmaps[0]['beatmapset_id']}/covers/cover.jpg")
        except:
            pass
        e.description = page_description[0]
        return [e, page_description, page_counter]