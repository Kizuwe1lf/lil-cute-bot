from bot_commands.c_main import stuff
import discord
from datetime import *
from scripts import *
from heapq import nlargest
import random


def osu_top(osu_user, message_author):
    get_user = stuff.get_user(osu_user)
    if not get_user:
        return f"~~{osu_user}~~ **was not found.**"
    else:
        try:
            get_best_scores = stuff.get_user_best1(osu_user)
            flag_url = f"https://osu.ppy.sh/images/flags/{get_user[0]['country']}.png"
            avatar_url = f"https://a.ppy.sh/{get_user[0]['user_id']}?{random.randint(100000, 999999)}"
            profile_url = f"https://osu.ppy.sh/u/{get_user[0]['user_id']}"
            e = discord.Embed(colour=message_author.colour)
            e.set_author(name=f"Top plays for {get_user[0]['username']}\n{get_user[0]['pp_raw']}pp (#{get_user[0]['pp_rank']} {get_user[0]['country']}{get_user[0]['pp_country_rank']})", url=profile_url, icon_url=flag_url)
            e.set_thumbnail(url=avatar_url)
            info = ""
            for play_rank in range(0, 3):
                player_combo_text = "x"
                player_combo_text += get_best_scores[play_rank]['maxcombo']
                if int(get_best_scores[play_rank]['perfect']) == 0:
                    player_combo_text = f"**{player_combo_text}**"
                score = get_score(get_best_scores[play_rank]['score'])
                beatmap = Beatmaps(get_best_scores[play_rank]['beatmap_id'], get_best_scores[play_rank]['enabled_mods'])
                get_beatmaps = stuff.get_beatmaps_osutop_edition(get_best_scores[play_rank]['beatmap_id'])
                count = get_best_scores[play_rank]['countmiss'], get_best_scores[play_rank]['count50'], get_best_scores[play_rank]['count100'], get_best_scores[play_rank]['count300']
                info += f"**{play_rank + 1}. [{get_beatmaps[0]['title'].replace('*', ' ')} [{get_beatmaps[0]['version']}]]"
                info += f"(https://osu.ppy.sh/beatmapsets/{get_beatmaps[0]['beatmapset_id']}#osu/{get_beatmaps[0]['beatmap_id']})\n"
                info += f"▸ [{beatmap.get_stars()}★]** +{num_to_mod(get_best_scores[play_rank]['enabled_mods'])} | {score} **-** {get_rank_emote(get_best_scores[play_rank]['rank'])}\n"
                info += f"▸ **{int(round(float(get_best_scores[play_rank]['pp'])))}**pp | ** {player_combo_text}/{get_beatmaps[0]['max_combo']}**\n"
                info += f"▸ {acc_calculator(*count):0.2f}% | {count[2]}x{get_onehundred_emote()} | {count[1]}x{get_fifty_emote()} | {count[0]}{get_miss_emote()}\n"
                info += f"▸ Score Set  {time_ago(datetime.strptime(get_best_scores[play_rank]['date'], '%Y-%m-%d %H:%M:%S'), datetime.utcnow())}\n"
            e.description = info
            return e
        except:
            return "Something went wrong"


def get_specific_play(osu_user, message_author, guild_id, given_play):
    get_best_scores = stuff.get_user_best1(osu_user)
    get_user = stuff.get_user(osu_user)
    if not get_user:  return f"~~{osu_user}~~ **was not found.**"
    if len(get_best_scores) < given_play:
        return f"**{get_user[0]['username']} has not submitted ~~{given_play}~~ plays yet.**"

    else:
        try:
            beatmap_id = get_best_scores[given_play - 1]['beatmap_id']
            get_beatmaps = stuff.get_beatmaps(beatmap_id, guild_id)
            e = discord.Embed(colour=message_author.colour)
            flag_url = f"https://osu.ppy.sh/images/flags/{get_user[0]['country']}.png"
            e.set_author(name=f"Top {given_play}. play for {get_user[0]['username']}\n{get_user[0]['pp_raw']}pp (#{get_user[0]['pp_rank']} {get_user[0]['country']}{get_user[0]['pp_country_rank']})", url=f"https://osu.ppy.sh/u/{get_user[0]['user_id']}", icon_url=flag_url)
            beatmap = Beatmaps(get_beatmaps[0]['beatmap_id'], int(get_best_scores[given_play - 1]['enabled_mods']))
            count = [get_best_scores[given_play - 1]['countmiss'], get_best_scores[given_play - 1]['count50'], get_best_scores[given_play - 1]['count100'], get_best_scores[given_play - 1]['count300']]
            fc_pp = ""
            player_combo_text = "x"
            player_combo_text += get_best_scores[given_play - 1]['maxcombo']
            if int(get_beatmaps[0]['max_combo']) - int(get_best_scores[given_play - 1]['maxcombo']) > 6 or int(count[0]) > 0:
                fc_pp = beatmap.get_if_fc_pp(no_choke_acc(*count))
            if get_best_scores[given_play - 1]['perfect'] == "0":
                player_combo_text = f"**{player_combo_text}**"
            score = get_score(get_best_scores[given_play - 1]['score'])
            info = f"**[{get_beatmaps[0]['title'].replace('*', ' ')}  [{get_beatmaps[0]['version']}]](https://osu.ppy.sh/beatmapsets/{get_beatmaps[0]['beatmapset_id']}#osu/{get_beatmaps[0]['beatmap_id']})**\n"
            info += f"▸ **[{beatmap.get_stars()}★]** +{num_to_mod(get_best_scores[given_play - 1]['enabled_mods'])} | {score} **-** {get_rank_emote(get_best_scores[given_play - 1]['rank'])}\n"
            info += f"▸ **{int(round(float(get_best_scores[given_play - 1]['pp'])))}**pp | {fc_pp} ** {player_combo_text}/{get_beatmaps[0]['max_combo']}**\n"
            info += f"▸ {acc_calculator(*count):0.2f}% | {count[2]}x{get_onehundred_emote()} | {count[1]}x{get_fifty_emote()} | {count[0]}{get_miss_emote()}\n"
            info += f"▸ Score Set  {time_ago(datetime.strptime(get_best_scores[given_play - 1]['date'], '%Y-%m-%d %H:%M:%S'), datetime.utcnow())}\n"
            # footer_text = f" idk what to put here"
            # e.set_footer(text=footer_text)
            e.set_thumbnail(url=f"https://a.ppy.sh/{get_user[0]['user_id']}")
            try:
                e.set_image(url=f"https://assets.ppy.sh/beatmaps/{get_beatmaps[0]['beatmapset_id']}/covers/cover.jpg")
            except:
                pass
            e.description = info
            return e
        except:
            return "Something went wrong!"


def get_latest_topplays(osu_user, message_author):
    get_best_scores = stuff.get_user_best1(osu_user)
    get_user = stuff.get_user(osu_user)
    dates = {}
    if not get_user:  return f"~~{osu_user}~~ **was not found.**"
    try:
        for play in range(len(get_best_scores)):
            dates[play] = [get_best_scores[play]['date']]
        play_list = nlargest(5, dates, key=dates.get)
        info = ""
        flag_url = f"https://osu.ppy.sh/images/flags/{get_user[0]['country']}.png"
        avatar_url = f"https://a.ppy.sh/{get_user[0]['user_id']}?{random.randint(100000, 999999)}"
        profile_url = f"https://osu.ppy.sh/u/{get_user[0]['user_id']}"
        e = discord.Embed(colour=message_author.colour)
        e.set_author(name=f"Most recent top plays for {get_user[0]['username']}\n{get_user[0]['pp_raw']}pp (#{get_user[0]['pp_rank']} {get_user[0]['country']}{get_user[0]['pp_country_rank']})", url=profile_url, icon_url=flag_url)
        e.set_thumbnail(url=avatar_url)
        for x in range(3):
            beatmap = Beatmaps(get_best_scores[play_list[x]]['beatmap_id'], int(get_best_scores[play_list[x]]['enabled_mods']))
            get_beatmaps = stuff.get_beatmaps_osutop_edition(get_best_scores[play_list[x]]['beatmap_id'])
            count = get_best_scores[play_list[x]]['countmiss'], get_best_scores[play_list[x]]['count50'], get_best_scores[play_list[x]]['count100'], get_best_scores[play_list[x]]['count300']
            score = get_score(get_best_scores[play_list[x]]['score'])
            player_combo_text = "x"
            player_combo_text += get_best_scores[play_list[x]]['maxcombo']
            if get_best_scores[play_list[x]]['perfect'] == "0":
                player_combo_text = f"**{player_combo_text}**"
            info += f"**{play_list[x] + 1}. [{get_beatmaps[0]['title'].replace('*', ' ')}  [{get_beatmaps[0]['version']}]]"
            info += f"(https://osu.ppy.sh/beatmapsets/{get_beatmaps[0]['beatmapset_id']}#osu/{get_beatmaps[0]['beatmap_id']})**\n"
            info += f"▸ **[{beatmap.get_stars()}★]** +{num_to_mod(get_best_scores[play_list[x]]['enabled_mods'])} | {score} **-** {get_rank_emote(get_best_scores[play_list[x]]['rank'])}\n"
            info += f"▸ **{int(round(float(get_best_scores[play_list[x]]['pp'])))}**pp | ** {player_combo_text}/{get_beatmaps[0]['max_combo']}**\n"
            info += f"▸ {acc_calculator(*count):0.2f}% | {count[2]}x{get_onehundred_emote()} | {count[1]}x{get_fifty_emote()} | {count[0]}{get_miss_emote()}\n"
            info += f"▸ Score Set  {time_ago(datetime.strptime(get_best_scores[play_list[x]]['date'], '%Y-%m-%d %H:%M:%S'), datetime.utcnow())}\n"
        e.description = info
        return e
    except:
        return "Something went wrong"
