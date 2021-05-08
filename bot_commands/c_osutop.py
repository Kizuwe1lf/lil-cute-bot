import discord
from datetime import *
from scripts import *
import numpy
import random


async def commands_osutop(ctx, player, request_obj):
    if player == None:
        await ctx.send('User Not Linked')
        return 0

    osu_username = player['osu_username']
    get_user = request_obj.get_user(osu_username)

    if not get_user:
        await ctx.send(f"~~{osu_username}~~ **was not found.**")
        return 0

    get_best_scores = request_obj.get_user_best1(osu_username)
    flag_url = f"https://osu.ppy.sh/images/flags/{get_user[0]['country']}.png"
    avatar_url = f"https://a.ppy.sh/{get_user[0]['user_id']}?{random.randint(100000, 999999)}"
    profile_url = f"https://osu.ppy.sh/u/{get_user[0]['user_id']}"
    e = discord.Embed(colour=ctx.message.author.colour)
    e.set_author(name=f"Top plays for {get_user[0]['username']}\n{get_user[0]['pp_raw']}pp (#{get_user[0]['pp_rank']} {get_user[0]['country']}{get_user[0]['pp_country_rank']})", url=profile_url, icon_url=flag_url)
    e.set_thumbnail(url=avatar_url)
    info = ""
    for play_rank in range(0, 3):
        player_combo_text = "x"
        player_combo_text += get_best_scores[play_rank]['maxcombo']
        if int(get_best_scores[play_rank]['perfect']) == 0:
            player_combo_text = f"**{player_combo_text}**"
        score = get_score(get_best_scores[play_rank]['score'])
        get_beatmaps = request_obj.get_beatmaps_osutop_edition(get_best_scores[play_rank]['beatmap_id'])
        count = get_best_scores[play_rank]['countmiss'], get_best_scores[play_rank]['count50'], get_best_scores[play_rank]['count100'], get_best_scores[play_rank]['count300']

        mods_list = num_to_mod_list(get_best_scores[play_rank]['enabled_mods'])
        mods_string = ''.join(mods_list)
        star_rating = get_difficulty(get_best_scores[play_rank]['beatmap_id'], mods_list)
        accuracy = calc_accuracy(*count)

        info += f"**{play_rank + 1}. [{get_beatmaps[0]['title'].replace('*', ' ')} [{get_beatmaps[0]['version']}]]"
        info += f"(https://osu.ppy.sh/beatmapsets/{get_beatmaps[0]['beatmapset_id']}#osu/{get_beatmaps[0]['beatmap_id']})\n"
        info += f"▸ [{star_rating}★]** +{mods_string} | {score} **-** {get_rank_emote(get_best_scores[play_rank]['rank'])}\n"
        info += f"▸ **{round_func(get_best_scores[play_rank]['pp'])}**pp | ** {player_combo_text}/{get_beatmaps[0]['max_combo']}**\n"
        info += f"▸ {accuracy}% | {count[2]}x{get_onehundred_emote()} | {count[1]}x{get_fifty_emote()} | {count[0]}{get_miss_emote()}\n"
        info += f"▸ Score Set  {time_ago(datetime.strptime(get_best_scores[play_rank]['date'], '%Y-%m-%d %H:%M:%S'), datetime.utcnow())}\n"
    e.description = info
    await send_embed(ctx, e)

async def commands_osutop_p(ctx, player, request_obj, given_play): # get specific play in user_best (users top100)
    if player == None:
        await ctx.send('User Not Linked')
        return 0

    osu_username = player['osu_username']
    get_best_scores = request_obj.get_user_best1(osu_username)
    get_user = request_obj.get_user(osu_username)

    if not get_user:
        await ctx.send(f"~~{osu_username}~~ **was not found.**")
        return 0
    if len(get_best_scores) < given_play:
        await ctx.send(f"**{get_user[0]['username']} has not submitted ~~{given_play}~~ plays yet.**")
        return 0

    beatmap_id = get_best_scores[given_play - 1]['beatmap_id']
    get_beatmaps = request_obj.get_beatmaps(beatmap_id, ctx.channel.id)
    e = discord.Embed(colour=ctx.message.author.colour)
    flag_url = f"https://osu.ppy.sh/images/flags/{get_user[0]['country']}.png"
    e.set_author(name=f"Top {given_play}. play for {get_user[0]['username']}\n{get_user[0]['pp_raw']}pp (#{get_user[0]['pp_rank']} {get_user[0]['country']}{get_user[0]['pp_country_rank']})", url=f"https://osu.ppy.sh/u/{get_user[0]['user_id']}", icon_url=flag_url)
    count = [get_best_scores[given_play - 1]['countmiss'], get_best_scores[given_play - 1]['count50'], get_best_scores[given_play - 1]['count100'], get_best_scores[given_play - 1]['count300']]

    mods_list = num_to_mod_list(get_best_scores[given_play - 1]['enabled_mods'])
    mods_string = ''.join(mods_list)
    star_rating = get_difficulty(get_best_scores[given_play - 1]['beatmap_id'], mods_list)
    accuracy = calc_accuracy(*count)

    fc_pp = ""
    player_combo_text = "x"
    player_combo_text += get_best_scores[given_play - 1]['maxcombo']
    if int(get_beatmaps[0]['max_combo']) - int(get_best_scores[given_play - 1]['maxcombo']) > 6 or int(count[0]) > 0:
        fc_pp_value = get_if_fc_pp(beatmap_id, mods_list, count)
        fc_pp = get_if_fc_pp_text(fc_pp_value['pp'])
    if get_best_scores[given_play - 1]['perfect'] == "0":
        player_combo_text = f"**{player_combo_text}**"
    score = get_score(get_best_scores[given_play - 1]['score'])
    info = f"**[{get_beatmaps[0]['title'].replace('*', ' ')}  [{get_beatmaps[0]['version']}]](https://osu.ppy.sh/beatmapsets/{get_beatmaps[0]['beatmapset_id']}#osu/{get_beatmaps[0]['beatmap_id']})**\n"
    info += f"▸ **[{star_rating}★]** +{mods_string} | {score} **-** {get_rank_emote(get_best_scores[given_play - 1]['rank'])}\n"
    info += f"▸ **{round_func(get_best_scores[given_play - 1]['pp'])}**pp | {fc_pp} ** {player_combo_text}/{get_beatmaps[0]['max_combo']}**\n"
    info += f"▸ {accuracy}% | {count[2]}x{get_onehundred_emote()} | {count[1]}x{get_fifty_emote()} | {count[0]}{get_miss_emote()}\n"
    info += f"▸ Score Set  {time_ago(datetime.strptime(get_best_scores[given_play - 1]['date'], '%Y-%m-%d %H:%M:%S'), datetime.utcnow())}\n"
    # footer_text = f" idk what to put here"
    # e.set_footer(text=footer_text)
    e.set_thumbnail(url=f"https://a.ppy.sh/{get_user[0]['user_id']}")
    try:
        e.set_image(url=f"https://assets.ppy.sh/beatmaps/{get_beatmaps[0]['beatmapset_id']}/covers/cover.jpg")
    except:
        pass
    e.description = info
    await send_embed(ctx, e)



async def commands_osutop_r(ctx, player, request_obj): # get latest top plays
    if player == None:
        await ctx.send('User Not Linked')
        return 0

    osu_username = player['osu_username']
    old_best_scores = request_obj.get_user_best1(osu_username)
    get_user = request_obj.get_user(osu_username)

    if not get_user:
        await ctx.send(f"~~{osu_username}~~ **was not found.**")
        return 0
    if not old_best_scores or len(old_best_scores) < 3:
        await ctx.send(f"Not Enough Scores")
        return 0

    get_best_scores = sorted(old_best_scores, key=lambda x:x['date'], reverse=True)

    info = ""
    flag_url = f"https://osu.ppy.sh/images/flags/{get_user[0]['country']}.png"
    avatar_url = f"https://a.ppy.sh/{get_user[0]['user_id']}?{random.randint(100000, 999999)}"
    profile_url = f"https://osu.ppy.sh/u/{get_user[0]['user_id']}"
    e = discord.Embed(colour=ctx.message.author.colour)
    e.set_author(name=f"Most recent top plays for {get_user[0]['username']}\n{get_user[0]['pp_raw']}pp (#{get_user[0]['pp_rank']} {get_user[0]['country']}{get_user[0]['pp_country_rank']})", url=profile_url, icon_url=flag_url)
    e.set_thumbnail(url=avatar_url)
    for play_rank in [0, 1, 2]:
        play_number = old_best_scores.index(get_best_scores[play_rank]) + 1
        get_beatmaps = request_obj.get_beatmaps_osutop_edition(get_best_scores[play_rank]['beatmap_id'])
        count = get_best_scores[play_rank]['countmiss'], get_best_scores[play_rank]['count50'], get_best_scores[play_rank]['count100'], get_best_scores[play_rank]['count300']

        mods_list = num_to_mod_list(get_best_scores[play_rank]['enabled_mods'])
        mods_string = ''.join(mods_list)
        star_rating = get_difficulty(get_best_scores[play_rank]['beatmap_id'], mods_list)
        accuracy = calc_accuracy(*count)

        score = get_score(get_best_scores[play_rank]['score'])
        player_combo_text = "x"
        player_combo_text += get_best_scores[play_rank]['maxcombo']
        if get_best_scores[play_rank]['perfect'] == "0":
            player_combo_text = f"**{player_combo_text}**"
        info += f"**{play_number}. [{get_beatmaps[0]['title'].replace('*', ' ')}  [{get_beatmaps[0]['version']}]]"
        info += f"(https://osu.ppy.sh/beatmapsets/{get_beatmaps[0]['beatmapset_id']}#osu/{get_beatmaps[0]['beatmap_id']})**\n"
        info += f"▸ **[{star_rating}★]** +{mods_string} | {score} **-** {get_rank_emote(get_best_scores[play_rank]['rank'])}\n"
        info += f"▸ **{round_func(get_best_scores[play_rank]['pp'])}**pp | ** {player_combo_text}/{get_beatmaps[0]['max_combo']}**\n"
        info += f"▸ {accuracy}% | {count[2]}x{get_onehundred_emote()} | {count[1]}x{get_fifty_emote()} | {count[0]}{get_miss_emote()}\n"
        info += f"▸ Score Set  {time_ago(datetime.strptime(get_best_scores[play_rank]['date'], '%Y-%m-%d %H:%M:%S'), datetime.utcnow())}\n"
    e.description = info
    await send_embed(ctx, e)
