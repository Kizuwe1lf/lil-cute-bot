from bot_commands.c_main import stuff
import discord
from datetime import *
from scripts import *
import random


async def commands_recent(ctx, player, update_bool):
    if player == None:
        await ctx.send('User Not Linked')
        return 0

    osu_username = player['osu_username']
    get_user = stuff.get_user(osu_username)
    get_recent = stuff.get_user_recent(osu_username)
    try_counter = 1

    if not get_user:
        await ctx.send(f"~~{osu_username}~~ **was not found.**")
        return 0
    if not get_recent:
        await ctx.send(f"~~{get_user[0]['username']}~~ **did not submit anything recently.**")
        return 0

    for x in range(len(get_recent)-1): # get Try counter by checking other recent plays
        if get_recent[0]['beatmap_id'] == get_recent[x + 1]['beatmap_id'] and get_recent[0]['enabled_mods'] == get_recent[x + 1]['enabled_mods']:
            try_counter += 1
        else:
            break

    get_beatmaps = stuff.get_beatmaps(get_recent[0]['beatmap_id'], ctx.channel.id) # request

    rank_text = "" # check if score on global leaderboards +1 request but its good
    get_scores = stuff.get_global(get_recent[0]['beatmap_id'], "")
    for x in range(len(get_scores)):
        if get_scores[x]['score'] == get_recent[0]['score'] and get_scores[x]['user_id'] == get_recent[0]['user_id']:
            rank_text = f"| Global**#{x+1}**"

    # for map completion im calculating total_hits also count array will make data easier to manipulate
    count = [get_recent[0]['countmiss'], get_recent[0]['count50'], get_recent[0]['count100'], get_recent[0]['count300']]
    total_hits = 0
    for item in count:
        total_hits += int(item)

    mods_list = num_to_mod_list(get_recent[0]['enabled_mods'])
    mods_string = ''.join(mods_list)

    maxcombo = get_recent[0]['maxcombo']

    get_pp_response = get_pp(get_recent[0]['beatmap_id'], mods_list, maxcombo, count)
    accuracy = get_pp_response['accuracy']

    pp_text = ""
    if get_recent[0]['rank'] != 'F': # dont include pp text if its fail play
        pp_text = get_pp_text(get_pp_response['pp'])

    score = get_score(get_recent[0]['score'])

    map_comp = get_map_completion(get_recent[0]['beatmap_id'], total_hits)
    fc_pp = ""

    if map_comp > 85:
        if int(get_beatmaps[0]['max_combo']) - int(get_recent[0]['maxcombo']) > 6 or int(count[0]) > 0 or get_recent[0]['rank'] == 'F': # add if fc pp to text if not fced
            fc_pp = get_if_fc_pp_text(get_if_fc_pp(get_recent[0]['beatmap_id'], mods_list, count)['pp'])

    player_combo_text = f"x{get_recent[0]['maxcombo']}"
    if get_recent[0]['perfect'] == "0": # make player combo text bold if max combo achieved
        player_combo_text = f"**{player_combo_text}**"

    if fc_pp == "" and pp_text == "":
        pp_text = f"<:msmile:586586198588522519> **-{random.randint(100, 500)}**pp"

    r_g_b = get_avg_colour_from_cover(get_beatmaps[0]['beatmapset_id'])  # get average rgb value from beatmap cover image
    e = discord.Embed(color=discord.colour.Colour.from_rgb(r_g_b[0], r_g_b[1], r_g_b[2]))

    flag_url = f"https://osu.ppy.sh/images/flags/{get_user[0]['country']}.png"
    e.set_author(name=f"{get_user[0]['username']}: {get_user[0]['pp_raw']}pp\n(#{get_user[0]['pp_rank']} {get_user[0]['country']}{get_user[0]['pp_country_rank']})", url=f"https://osu.ppy.sh/u/{get_user[0]['user_id']}", icon_url=flag_url)
    try:
        e.set_image(url=f"https://assets.ppy.sh/beatmaps/{get_beatmaps[0]['beatmapset_id']}/covers/cover.jpg")
    except:
        pass
    avatar_url = f"https://a.ppy.sh/{get_user[0]['user_id']}?{random.randint(100000, 999999)}"  # im adding ?xxxxxx to avatar url because this way discord can't cache avatars
    e.set_thumbnail(url=avatar_url)

    star_rating = get_difficulty(get_recent[0]['beatmap_id'], mods_list)

    # embed description the all information i have collected above
    info = f"**[{get_beatmaps[0]['title'].replace('*', ' ')} [{get_beatmaps[0]['version']}]](https://osu.ppy.sh/beatmapsets/{get_beatmaps[0]['beatmapset_id']}#osu/{get_beatmaps[0]['beatmap_id']})**\n"
    info += f"▸ **[{star_rating}★]** +{mods_string} | {score} **-** {get_rank_emote(get_recent[0]['rank'])}\n"
    info += f"▸  {pp_text} {fc_pp} ** {player_combo_text}/{get_beatmaps[0]['max_combo']}**\n"
    info += f"▸ {get_pp_response['accuracy']}% | {count[2]}x{get_onehundred_emote()} | {count[1]}x{get_fifty_emote()} | {count[0]}{get_miss_emote()}\n"
    info += f"▸ Try **#{try_counter}** | {time_ago(datetime.strptime(get_recent[0]['date'], '%Y-%m-%d %H:%M:%S'), datetime.utcnow())} {rank_text}\n"
    if get_recent[0]['rank'] == 'F': info += f"▸ Map Completion: {map_comp}%\n"
    # footer_text = f" idk what to put here"
    # e.set_footer(text=footer_text)
    e.description = info
    await send_embed(ctx, e)
    if update_bool == True:
        db_obj = Database()
        user_data = db_obj.preparing_user_data_for_db_functions(get_user, ctx.message.author.id, player['servers'], ctx.guild.id)
        db_obj.update_after_play(user_data)
