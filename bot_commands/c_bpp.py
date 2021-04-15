from bot_commands.c_main import stuff


async def commands_bpp(ctx, player):
    if player == None:
        await ctx.send('User Not Linked')
        return 0

    osu_username = player['osu_username']
    get_best_scores = stuff.get_user_best1(osu_username)
    get_user = stuff.get_user(osu_username)

    if not get_user:
        await ctx.send(f"~~{osu_username}~~ **was not found.**")
        return 0

    bonus_pp = 0
    for play in range(len(get_best_scores)):
        bonus_pp += float(get_best_scores[play]['pp']) * (0.95 ** play) # pp weight formula
    now_pp = float(get_user[0]['pp_raw'])
    bonus_pp = now_pp - bonus_pp
    await ctx.send(f"**{get_user[0]['username']}** has **{round_func(bonus_pp)}** bonus pp")
