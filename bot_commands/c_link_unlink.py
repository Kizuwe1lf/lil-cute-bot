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
        await ctx.send('Linked <:mpeepohappy:859122493902159902>')
    else: # if in db
        if ctx.guild.id in user_data_in_db['servers']:
            await ctx.send('Already Linked! <:rampout:859121516507955200>')
        else:
            user_data_in_db['servers'] += [ctx.guild.id]
            db_obj.update_data(user_data_in_db)
            await ctx.send(f'Now recognizing you in {ctx.guild.name} too! <:shades:859121515529502760>')

async def commands_unlink(ctx, db_obj):
    db_obj.delete_data(ctx.message.author.id)
    await ctx.send('<:sadignored:859121512119926794>')
