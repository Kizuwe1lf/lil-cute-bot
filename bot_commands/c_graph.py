from datetime import datetime, timedelta
from make_chart import make_chart

async def commands_graph(ctx, db_obj, osu_username, field_name_text, day):
    field_names_in_db = ['pp_raw' , 'pp_rank', 'accuracy', 'playcount', 'pp_country_rank']
    field_names_from_user = ['pp' , 'rank', 'acc', 'pc', 'countryrank']

    if field_name_text not in field_names_from_user:
        return await ctx.send('Wrong field usage available ones are; pp, rank, acc, pc, countryrank')


    if day == 'all':
        day = 2000
    elif int(day) < 5:
        return await ctx.send('Use minimum 7 days')

    day = int(day)
    index = field_names_from_user.index(field_name_text)
    field_name = field_names_in_db[index]

    cursor = db_obj.search_date(osu_username, day)  # if day == 7 this means weekly chart if day == 30 this means monthly chart

    value_array = []
    date_array = []

    if cursor.count() == 0:
        return await ctx.send(f'I could not find any data related to {osu_username}! Use more recent command so i can have some data <:hyperEvil:496683825859002368>')

    elif cursor.count() < 3:
        return await ctx.send('Not Enough Data! Use more recent command so i can have some data <:hyperEvil:496683825859002368>')

    discord_id = cursor[0]['discord_id']
    osu_username = cursor[0]['osu_username']

    servers = db_obj.select_players_by_id(discord_id)['servers']

    if ctx.message.guild.id not in servers:
        return await ctx.send(f'I dont recognize {osu_username} from this server')


    for row in cursor:
        date_array.append(row['date'])
        value_array.append(row[field_name])


    if abs(value_array[0] - value_array[-1]) < 1.5:
        return await ctx.send('Not Enough Change')

    reverse = False
    if field_name == 'pp_rank' or field_name == 'pp_country_rank':
        reverse = True

    title = f"{field_name_text} line chart for {osu_username}"
    await make_chart(ctx, date_array, value_array, title, reverse)
