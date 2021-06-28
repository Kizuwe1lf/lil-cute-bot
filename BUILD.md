How to build lil-cute-bot

## Dependencies

```
Python 3.6+ (with requirements.txt)
Net Core 3.1+
MongoDB Online DB
```

## MongoDB
```
You need a online MongoDB Cluster
Your DB needs 3 Collections/Tables
Default names are:

Database name = "lil_cute_db"
Collection 1 name = "users_main"
Collection 2 name = "users_history"
Collection 3 name = "prefixes"

You might wanna change default names, if so check Database.py L#13, L#14, L#15, L#16
```

## .env File

Your .env File must look like this.

```
MONGO_DB_STRING=      // mongo db connection uri
BOT_TOKEN=            // discord bot token
API_KEY=              // osu api key
```

# Constants

You might wanna change constants.

```
main.py L#32       // bot invite link
main.py L#33       // bot default channel id
```

## Emotes

If you wanna fully build lil-cute-bot you need discord emotes.
You have 2 way of getting lil-cute-bot emotes.

```
Way 1 : Join my bot emote server download emotes and change emote strings in project (thats a lot of work)
Way 2 : Contact me via discord or somethin else so i can invite your bot into my emote server
```
Emote server invite [link](https://discord.gg/YcfRSmy8Jp).
