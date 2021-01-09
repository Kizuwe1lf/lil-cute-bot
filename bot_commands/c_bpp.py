from bot_commands.c_main import stuff


def get_bpp(osu_user):
    try:
        get_best_scores = stuff.get_user_best1(osu_user)
        get_user = stuff.get_user(osu_user)
        bonus_pp = 0
        for z in range(len(get_best_scores)):
            bonus_pp += float(get_best_scores[z]['pp']) * (0.95 ** z)
        now_pp = float(get_user[0]['pp_raw'])
        bonus_pp = now_pp - bonus_pp
        return f"**{get_user[0]['username']}** has **{round(float(bonus_pp), 2)}** bonus pp"
    except:
        return "Something went wrong!"
