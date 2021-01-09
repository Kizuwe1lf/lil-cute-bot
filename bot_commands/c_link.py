from bot_commands.c_main import stuff
from database import *


def get_data(osu_user, discord_id):
    my_list = [discord_id, osu_user[0]['username'], int(osu_user[0]['user_id']), int(osu_user[0]['pp_rank']), float(osu_user[0]['pp_raw']), int(osu_user[0]['pp_country_rank']), osu_user[0]['country'], float(osu_user[0]['accuracy'])]
    return my_list
    


def link1(osu_user, discord_id):
    db_object = Database()
    check_if_linked = db_object.select_from_database(discord_id)
    if check_if_linked != 'User not linked':
        return "Already Linked!"
    else:
        get_user = stuff.get_user(osu_user)
        my_data = get_data(get_user, discord_id)
        output = db_object.insert_into_database(my_data)
        db_object.close_connection()
        return output

   

def unlink1(discord_id):
    db_object = Database()
    db_object.delete_from_database(discord_id)
    db_object.close_connection()
    return 'k'
