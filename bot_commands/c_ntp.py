from bot_commands.c_main import stuff

def get_list_of_pp(arr):
    pp = []
    for play in arr:
        pp.append(float(play['pp']))
    return pp

def calculate_total_pp(arr):
    i = 0
    total_pp = 0
    while i < len(arr):
        total_pp += arr[i] * (0.95 ** i)  # PP Weight Formula
        i += 1
    return total_pp

def sort_pp_list(arr):
    arr.sort(reverse = True)
    return arr

def get_ntps(pp_tuple, pp_list): # when len(given_tuple) > 1
    given_pp_list = []
    for pp_value in pp_tuple:
        given_pp_list.append(float(pp_value))

    given_pp_list = sort_pp_list(given_pp_list)
    plays_added = 0

    for pp in given_pp_list:
        index = -1 - plays_added
        if pp > pp_list[index]:
            pp_list[index] = pp
            plays_added += 1
    pp_list = sort_pp_list(pp_list)
    return pp_list, plays_added

async def commands_ntp(ctx, player, pp_tuple):
    if player == None:
        await ctx.send('User Not Linked')
        return 0
    osu_username = player['osu_username']

    get_best_scores = stuff.get_user_best1(osu_username)
    get_user = stuff.get_user(osu_username)
    if not get_user:
        await ctx.send(f"~~{osu_username}~~ **was not found.**")
        return 0

    pp_list = get_list_of_pp(get_best_scores)
    bonus_pp = calculate_total_pp(pp_list)

    now_pp = float(get_user[0]['pp_raw']) # defalt raw pp
    bonus_pp = now_pp - bonus_pp          # bonus_pp = default raw pp - default raw pp that i calculated (this works cause we cant calculate bonus pp)
    total_pp = bonus_pp                   # total_pp has bonus_pp now imma do += to total pp now

    more_than_one = False
    if len(pp_tuple) < 2:
        given_pp = float(pp_tuple[0])
        if given_pp > pp_list[-1]:
            pp_list[-1] = given_pp
            pp_list = sort_pp_list(pp_list)
            play_number = pp_list.index(given_pp) + 1
        else:
            await ctx.send(f"This play wont give **{get_user[0]['username']}** any pp")
            return 0
    else:
        return_value = get_ntps(pp_tuple, pp_list)
        pp_list = return_value[0]
        plays_added = return_value[1]

        more_than_one = True
        if plays_added < 1:
            await ctx.send(f"These plays wont give **{get_user[0]['username']}** any pp")
            return 0
    total_pp += calculate_total_pp(pp_list) # += because it has bonus_pp
    pp_increase = total_pp - now_pp
    if not more_than_one:
        await ctx.send(f"**{round_func(given_pp)}**pp play would be **{get_user[0]['username']}**'s **#{play_number}** Personal Best. Total pp achieved would be **{round_func(total_pp)}**pp. **(+{round_func(pp_increase)})**")
    else:
        await ctx.send(f"**{plays_added}** plays added to **{get_user[0]['username']}**'s top plays  Total pp achieved would be **{round_func(total_pp)}**pp  **(+{round_func(pp_increase)})**")
