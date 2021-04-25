import os
import pymongo
from datetime import datetime
from datetime import timedelta
from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv

class Database():
    def __init__(self):
        load_dotenv(find_dotenv())
        cluster = MongoClient(os.getenv('MONGO_DB_STRING'))

        db = cluster["lil_cute_db"]
        self.users = db["users_main"]
        self.user_history = db["users_history"] # for tracking data changes
        self.prefixes = db["prefixes"]

    def update_data(self, user_data):
        where = { "osu_user_id": user_data["osu_user_id"] }
        set = { "$set": user_data }
        self.users.update_one(where, set)

    def insert_data(self, user_data):
        self.users.insert_one(user_data)
        self.insert_history_collection(user_data)

    def delete_data(self, discord_id):
        where = { "discord_id": discord_id }
        self.users.delete_one(where)

    def select_players_by_id(self, discord_id):
        where = { "discord_id": discord_id }
        result = self.users.find_one(where)
        return result

    def select_players_by_server(self, server_id):
        where = {"servers" : { "$in": [server_id] } }
        return self.users.find(where)

    def update_after_play(self, user_data):
        self.update_data(user_data)
        self.insert_history_collection(user_data)

    def insert_history_collection(self, user_data):
        user_data['date'] = datetime.now()

        self.user_history.insert_one(user_data)

    def preparing_user_data_for_db_functions(self, get_user, discord_id, servers, server_id): # for first insert servers must be empty list
        if server_id not in servers:
            servers += [server_id]

        user_data = {
            "discord_id": discord_id,
            "osu_username": get_user[0]['username'],
            "osu_user_id" : get_user[0]['user_id'],
            "pp_rank" : int(get_user[0]['pp_rank']),
            "pp_raw" : float(get_user[0]['pp_raw']),
            "pp_country_rank" : int(get_user[0]['pp_country_rank']),
            "accuracy" : float(get_user[0]['accuracy']),
            "playcount" : int(get_user[0]['playcount']),
            "country" : get_user[0]['country'],
            "ranked_score" : int(get_user[0]['ranked_score']),
            "total_score" : int(get_user[0]['total_score']),
            "count300" : int(get_user[0]['count300']),
            "count100" : int(get_user[0]['count100']),
            "count50" : int(get_user[0]['count50']),
            "servers" : servers
        }
        return user_data

    def set_prefix(self, server_id, prefix):
        result = self.get_prefix(server_id)

        data = {
            "server_id": server_id,
            "prefix": prefix
        }

        if result[1] == 1: # updates prefix if it exists
            where = { "server_id": server_id }
            set = { "$set": data }
            self.prefixes.update_one(where, set)
        else:
            self.prefixes.insert_one(data)

        return prefix

    def get_prefix(self, server_id):
        where = { "server_id": server_id }
        result = self.prefixes.find_one(where)
        if result is not None:
            return [result['prefix'], 1]
        return ['>', 0]

    def search_date(self, osu_username, day):
        today = datetime.now()
        first_day = today - timedelta(day)
        cursor = self.user_history.find({"osu_username": {'$regex' : osu_username, '$options' : 'i'}, "date": {"$gt": first_day}})
        return cursor, first_day, today
