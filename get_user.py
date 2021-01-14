from database import *


def get_osu_user_from_db(discord_id):
    db_object = Database()
    osu_user = db_object.select_from_database(discord_id)
    db_object.close_connection()
    return osu_user
    
    
def update_user(discord_id, data):
    db_object = Database()
    my_data = [discord_id, data[0]['username'], None, int(data[0]['pp_rank']), float(data[0]['pp_raw']), int(data[0]['pp_country_rank']), data[0]['country'], float(data[0]['accuracy'])]
    db_object.update_database(my_data)
    db_object.close_connection()