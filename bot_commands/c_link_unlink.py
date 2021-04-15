from bot_commands.c_main import stuff


async def commands_link(ctx, osu_username, db_obj):
    check_if_linked = db_obj.select_players_by_id(ctx.message.author.id)

    if check_if_linked != None:
        await ctx.send("Already Linked!")
        return 0

    get_user = stuff.get_user(osu_username)

    if not get_user:
        await ctx.send("User Not Found")
        return 0

    user_data = db_obj.preparing_user_data_for_db_functions(get_user, ctx.message.author.id, [], ctx.guild.id)
    output = db_obj.insert_data(user_data)
    await ctx.send('Linked <:mpeepoHappy:701361814738305095>')

async def commands_unlink(ctx, db_obj):
    db_obj.delete_data(ctx.message.author.id)
    await ctx.send('<:sadIgnored:530917237406826496>')