async def commands_link(ctx, osu_username, request_obj, db_obj):
    user_data_in_db = db_obj.select_players_by_id(ctx.message.author.id)

    if user_data_in_db is None: # if none link it
        if osu_username == None:
            return await ctx.send('Wheres ur username bud')

        get_user = request_obj.get_user(osu_username)

        if not get_user:
            return await ctx.send("User Not Found")

        user_data = db_obj.preparing_user_data_for_db_functions(get_user, ctx.message.author.id, [], ctx.guild.id)
        db_obj.insert_data(user_data)
        await ctx.send('Linked <:mpeepoHappy:701361814738305095>')
    else: # if in db
        if ctx.guild.id in user_data_in_db['servers']:
            await ctx.send('Already Linked! <:ramPout:716183173318443018>')
        else:
            user_data_in_db['servers'] += [ctx.guild.id]
            db_obj.update_data(user_data_in_db)
            await ctx.send(f'Now recognizing you in {ctx.guild.name} too! <:shades:627100412851388426>')

async def commands_unlink(ctx, db_obj):
    db_obj.delete_data(ctx.message.author.id)
    await ctx.send('<:sadIgnored:530917237406826496>')
