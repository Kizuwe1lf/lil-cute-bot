import sqlite3


class Database:
    def __init__(self):
        self.conn = sqlite3.connect('my_files\lil_cute.db')
        self.cursor = self.conn.cursor()
        
    def create_table(self):
        self.conn.execute('''CREATE TABLE osu_userDB
         (
         discord_id INT PRIMARY KEY,
         username           TEXT,
         osu_user_id        INT,
         pp_rank        INT,
         pp_raw         REAL,
         pp_country_rank   INT,
         country          TEXT,
         accuracy         REAL
         );''') 

    def insert_into_database(self, data):
        command = "INSERT INTO osu_userDB (discord_id, username, osu_user_id, pp_rank, pp_raw, pp_country_rank, country, accuracy) Values (?, ?, ?, ?, ?, ?, ?, ?)"
        args = (data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7])
        self.cursor.execute(command, args)
        self.conn.commit()
        return "Linked"

    def update_database(self, data):
        command = "UPDATE osu_userDB SET username=?, pp_rank=?, pp_raw=?, pp_country_rank=?, country=?, accuracy=? WHERE discord_id=?"
        args = (data[1], data[3], data[4], data[5], data[6], data[7], data[0])
        self.cursor.execute (command, args)
        self.conn.commit()
        
    def select_from_database(self, discord_id):
        command = "SELECT username FROM osu_userDB WHERE discord_id=?"
        args = (discord_id,)
        self.cursor.execute(command, args)
        try:
            username = self.cursor.fetchone()[0]
        except:
            username = 'User not linked'
        return username

    def delete_from_database(self, discord_id):
        command = "DELETE FROM osu_userDB WHERE discord_id=?"
        args = (discord_id,)
        self.cursor.execute(command, args)
        self.conn.commit()
        return "Unlinked"
        
    def multiple_select_from_database(self, discord_id):
        player_list = []
        for d_id in discord_id:
            command = "SELECT * FROM osu_userDB WHERE discord_id=?"
            args = (d_id,)
            self.cursor.execute(command, args)
            x = self.cursor.fetchone()
            if x:
                player_list.append(x)
        return player_list
        
    def close_connection(self):
        self.conn.close()


# xd = Database()    # one time execution
# xd.create_table()  # one time execution
