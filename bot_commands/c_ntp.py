from bot_commands.c_main import stuff


def get_ntp(osu_user, given_tuple):
    given_pp = []
    for x in range(len(given_tuple)):
        given_pp.append(float(given_tuple[x]))
    get_best_scores = stuff.get_user_best1(osu_user)
    get_user = stuff.get_user(osu_user)
    pp = []
    if not get_user:  return f"~~{osu_user}~~ **was not found.**"
    try:
        bonus_pp = 0
        for z in range(len(get_best_scores)):
            bonus_pp += float(get_best_scores[z]['pp']) * (0.95 ** z)
            pp.append(float(get_best_scores[z]['pp']))
        now_pp = float(get_user[0]['pp_raw'])
        bonus_pp = now_pp - bonus_pp
        total_pp = bonus_pp
        multi_given_pp = False
        if len(given_pp) < 2:
            given_pp = given_pp[0]
            if given_pp > pp[-1]:
                del pp[-1]
                pp.append(given_pp)
                pp.sort(reverse = True)
                play_number = pp.index(given_pp) + 1
            else: return f"This play wont give **{get_user[0]['username']}** any pp"
        else:
            good_variable = get_new_top_plays(given_pp, pp)
            multi_given_pp = True
            pp = good_variable[0]
            if good_variable[1] < 1: return f"These plays wont give **{get_user[0]['username']}** any pp"
        for z in range(len(pp)):
            total_pp += pp[z] * (0.95 ** z)
        pp_increase = total_pp - now_pp
        if not multi_given_pp:
            return f"**{round(float(given_pp), 2)}**pp play would be **{get_user[0]['username']}**'s **#{play_number}** Personal Best. Total pp achieved would be **{round(total_pp, 2)}**pp. **(+{round(pp_increase, 2)})**"
        else:
            return f"**{good_variable[1]}** plays added to **{get_user[0]['username']}**'s top plays  Total pp achieved would be **{round(total_pp,2)}**pp  **(+{round(pp_increase, 2)})**"
    except:
        return "Something went wrong!"

        
        
def get_new_top_plays(given_pp_list, pp): # fixed
    added_pp_list = []
    plays_added = 0
    given_pp_list = sorted(given_pp_list, reverse=True)
    for item in given_pp_list:
        if item > pp[99-plays_added]:
            plays_added += 1
            added_pp_list.append(item)
    del pp[-len(added_pp_list):]
    pp.extend(added_pp_list)
    pp.sort(reverse = True)
    return pp, plays_added