from datetime import datetime, timedelta
from make_chart import make_chart

async def commands_graph(ctx, db_obj, osu_username, field_name_text, day):
    field_names_in_db = ['pp_raw' , 'pp_rank', 'accuracy', 'playcount', 'pp_country_rank']
    field_names_from_user = ['pp' , 'rank', 'acc', 'playcount', 'countryrank']

    if field_name_text not in field_names_from_user:
        return await ctx.send('Wrong field usage available ones are; pp, rank, acc, playcount, countryrank')

    if day < 5:
        return await ctx.send('Use minimum 7 days')

    if day > 90:
        return await ctx.send('Use minimum 90 days')

    index = field_names_from_user.index(field_name_text)
    field_name = field_names_in_db[index]


    cursor, first_day, last_day = db_obj.search_date(osu_username, day)  # if day == 7 this means weekly chart if day == 30 this means monthly chart

    value_array = []
    date_array = []

    if cursor.count() == 0:
        return await ctx.send(f'I could not find any data related to {osu_username}')

    discord_id = cursor[0]['discord_id']
    osu_username = cursor[0]['osu_username']

    need_day = first_day
    first_data_day = cursor[0]['date']

    if need_day < first_data_day:
        need_day = first_data_day - timedelta(1)

    servers = db_obj.select_players_by_id(discord_id)['servers']

    if ctx.message.guild.id not in servers:
        return await ctx.send(f'I dont recognize {osu_username} from this server')

    last_added_day = 999

    for row in cursor:
        while need_day.day < row['date'].day:
            need_day += timedelta(1)

        if last_added_day == row['date'].day:
            value_array[-1] = row[field_name]
            continue

        if need_day.day == row['date'].day:
            date_array.append(f"{need_day.strftime('%h')} {need_day.day}")
            value_array.append(row[field_name])
            last_added_day = row['date'].day
            need_day += timedelta(1)


    if len(date_array) < 3:
        return await ctx.send('Not Enough Data')

    if abs(value_array[0] - value_array[-1]) < 2:
        return await ctx.send('Not Enough Change')

    title = f"{field_name_text} line chart for {osu_username}"
    await make_chart(ctx, date_array, value_array, title, 'Date', field_name_text)
