from bot_commands.c_main import stuff
import discord
from datetime import *
from scripts import *
import random


async def commands_compare(ctx, player, bot):
    if player == None:
        await ctx.send('User Not Linked')
        return 0

    osu_username = player['osu_username']
    beatmap_id = stuff.get_beatmap_id(ctx.channel.id)
    get_user = stuff.get_user(osu_username)
    get_scores = stuff.get_scores(osu_username, beatmap_id, ctx.channel.id)

    if not beatmap_id:
        await ctx.send(f"Theres no ~~beatmap_id~~ in cache")
        return 0
    if not get_user:
        await ctx.send(f"~~{osu_username}~~ **was not found.**")
        return 0
    if not get_scores:
         await ctx.send(f"~~{get_user[0]['username']}~~ **has no scores on the map.**")
         return 0

    page_counter = 1
    page_description = []
    get_beatmaps = stuff.get_beatmaps(beatmap_id, ctx.channel.id)
    r_g_b = get_avg_colour_from_cover(get_beatmaps[0]['beatmapset_id'])
    flag_url = f"https://osu.ppy.sh/images/flags/{get_user[0]['country']}.png"
    e = discord.Embed(color=discord.colour.Colour.from_rgb(r_g_b[0], r_g_b[1], r_g_b[2]))
    info = f"**[{get_beatmaps[0]['title'].replace('*', ' ')} [{get_beatmaps[0]['version']}]](https://osu.ppy.sh/beatmapsets/{get_beatmaps[0]['beatmapset_id']}#osu/{get_beatmaps[0]['beatmap_id']})**\n"
    e.set_author(name=f"Top plays on this map for {get_scores[0]['username']}\n{get_user[0]['pp_raw']}pp (#{get_user[0]['pp_rank']} {get_user[0]['country']}{get_user[0]['pp_country_rank']})", url=f"https://osu.ppy.sh/u/{get_user[0]['user_id']}", icon_url=flag_url)
    counter = 0
    for play in get_scores:
        counter += 1
        if counter % 4 == 0:
            page_description.append(info)
            info = f"**[{get_beatmaps[0]['title'].replace('*', ' ')} [{get_beatmaps[0]['version']}]](https://osu.ppy.sh/beatmapsets/{get_beatmaps[0]['beatmapset_id']}#osu/{get_beatmaps[0]['beatmap_id']})**\n"
            page_counter += 1
        count = [play['countmiss'], play['count50'], play['count100'], play['count300']]
        score = get_score(play['score'])

        accuracy = calc_accuracy(*count)
        mods_list = num_to_mod_list(play['enabled_mods'])
        mods_string = ''.join(mods_list)

        player_combo_text = "x"
        player_combo_text += play['maxcombo']
        if play['perfect'] == "0":
            player_combo_text = f"**{player_combo_text}**"

        fc_pp = ""
        if int(get_beatmaps[0]['max_combo']) - int(play['maxcombo']) > 6 or int(count[0]) > 0:
            fc_pp_value = get_if_fc_pp(beatmap_id, mods_list, count)
            fc_pp = get_if_fc_pp_text(fc_pp_value['pp'])

        if play['pp'] is not None:
            pp_text = f"**{float(play['pp']):0.2f}**pp"
        else:
            pp_value = get_pp(beatmap_id, mods_list, play['maxcombo'], count)
            pp_text = get_pp_text(pp_value['pp'])

        info += f"▸ **[{get_difficulty(beatmap_id, mods_list)}★]** +{mods_string} | {score} **-** {get_rank_emote(play['rank'])} \n"
        info += f"▸ {pp_text} {fc_pp} ** {player_combo_text}/{get_beatmaps[0]['max_combo']}**\n"
        info += f"▸ {accuracy}% | {count[2]}x{get_onehundred_emote()} | {count[1]}x{get_fifty_emote()} | {count[0]}{get_miss_emote()}\n"
        info += f"▸ Score Set {time_ago(datetime.strptime(play['date'], '%Y-%m-%d %H:%M:%S'), datetime.utcnow())}\n \n"
    page_description.append(info)
    avatar_url = f"https://a.ppy.sh/{get_user[0]['user_id']}?{random.randint(100000, 999999)}"
    e.set_thumbnail(url=avatar_url)
    try:
        e.set_image(url=f"https://assets.ppy.sh/beatmaps/{get_beatmaps[0]['beatmapset_id']}/covers/cover.jpg")
    except:
        pass
    e.description = page_description[0]
    if page_counter > 1:
        await send_pages(ctx, e, page_description, page_counter)
    else:
        await send_embed(ctx, e)
