import discord

async def commands_help(ctx, prefix, command_name, bot_user_name):
    output = "```"

    if command_name == 'acc':
        output += "Shows pp value for last specified beatmap\n"
        output += f"If you wanna change last specified beatmap simply use {prefix}map command\n"
        output += "Example Usages\n\n"
        output += f"{prefix}acc 0 35 hddt"
        output += f"{prefix}acc 5 4"

    elif command_name == 'link':
        output += "Links your osu account to your discord account\n"
        output += "Benefits are you dont have to type osu_username parameter it automatically detects\n"
        output += "Theres special commands for linked players ex: cs, graph, leaderboards\n"
        output += "Example Usages\n\n"
        output += f"{prefix}link osu_username\n"
        output += f"{prefix}link      description: if you wanna recognize by bot from different servers simply use this command on these servers"

    elif command_name == 'unlink':
        output += "Unlinks your account\n"
        output += "Example Usage\n\n"
        output += f"{prefix}unlink"

    elif command_name == 'osu':
        output += "Shows osu profile of given player\n"
        output += "Example Usages\n\n"
        output += f"{prefix}osu osu_username\n"
        output += f"{prefix}osu osu_username1 osu_username2 osu_username3...\n\n"
        output += "instead of osu_username u can mention linked users or you just dont give any username for self use\n"
        output += f"Examples: {prefix}{command_name} @discord_user or {prefix}{command_name}"

    elif command_name == 'osutop':
        output += "Shows top plays for given username\n"
        output += "Example Usages\n\n"
        output += f"{prefix}osutop osu_username\n"
        output += f"{prefix}osutop osu_username p 15      description: shows 15th play for given user\n"
        output += f"{prefix}osutop osu_username r         description: shows latest 3 top plays for given user\n\n"
        output += "instead of osu_username u can mention linked users or you just dont give any username for self use\n"
        output += f"Examples: {prefix}{command_name} @discord_user or {prefix}{command_name}"

    elif command_name == 'recent':
        output += "Shows most recent score for given username\n"
        output += "Example Usage\n"
        output += f"{prefix}recent osu_username\n\n"
        output += "instead of osu_username u can mention linked users or you just dont give any username for self use\n"
        output += f"Examples: {prefix}{command_name} @discord_user or {prefix}{command_name}"

    elif command_name == 'compare':
        output += "Shows scores of given username for the last specified beatmap\n"
        output += f"If you wanna change last specified beatmap simply use {prefix}map command\n"
        output += "Example Usage\n"
        output += f"{prefix}compare osu_username\n\n"
        output += "instead of osu_username u can mention linked users or you just dont give any username for self use\n"
        output += f"Examples: {prefix}{command_name} @discord_user or {prefix}{command_name}"

    elif command_name == 'compareserver':
        output += "Shows best 8 scores made by linked players in the server for last specified beatmap\n"
        output += f"If you wanna change last specified beatmap simply use {prefix}map command\n"
        output += "Example Usage\n"
        output += f"{prefix}compareserver"

    elif command_name == 'global':
        output += "Shows global best 8 scores for the last specified beatmap\n"
        output += f"If you wanna change last specified beatmap simply use {prefix}map command\n"
        output += "Example Usages\n\n"
        output += f"{prefix}global\n"
        output += f"{prefix}global hddt"

    elif command_name == 'ntp':
        output += "Adds given pp value to given player's top plays and simulates their new overall pp\n"
        output += "Example Usages\n\n"
        output += f"{prefix}ntp osu_username 500\n"
        output += f"{prefix}ntp osu_username 500 500 500 500\n\n"
        output += "instead of osu_username u can mention linked users or you just dont give any username for self use\n"
        output += f"Examples: {prefix}{command_name} @discord_user or {prefix}{command_name}"

    elif command_name == 'bpp':
        output += "Shows bonus pp of given player's pp\n"
        output += "Example Usages\n\n"
        output += f"{prefix}bpp osu_username\n\n"
        output += "instead of osu_username u can mention linked users or you just dont give any username for self use\n"
        output += f"Examples: {prefix}{command_name} @discord_user or {prefix}{command_name}"

    elif command_name == 'leaderboards':
        output += "Shows stat leaderboards for server\n"
        output += "Example Usage\n\n"
        output += f"{prefix}leaderboards"

    elif command_name == 'globalboards':
        output += f"Shows stat leaderboards for everyone linked with {bot_user_name}\n"
        output += f"Example Usage\n\n"
        output += f"{prefix}globalboards"

    elif command_name == "map":
        output += f"Shows beatmap info\n"
        output += f"Mostly used for changing last specified beatmap\n"
        output += f"Example Usages\n\n"
        output += f"{prefix}map beatmap_link\n"
        output += f"{prefix}map             description: info for last specified beatmap\n"
        output += f"{prefix}map 123456      description: 123456 are beatmap id\n"

    elif command_name == "roll":
        output += "Random random random numbers! fun command\n"
        output += "Example Usages\n\n"
        output += f"{prefix}roll          description: rolls between 1-100\n"
        output += f"{prefix}roll 150      description: rolls between 1-150\n"
        output += f"{prefix}roll iq       description: best usage LOL"

    elif command_name == "aliases":
        output += "Shows commands aliases\n"
        output += "Example Usage\n\n"
        output += f"{prefix}aliases"

    elif command_name == "setprefix":
        output += "Changes bot prefix for server administrator only\n"
        output += "Example Usages\n\n"
        output += f"{prefix}setprefix new_prefix"

    elif command_name == "graph":
        output += "Shows really cool line chart for given player\n"
        output += "Only works for linked users\n"
        output += "Example Usages\n\n"
        output += f"{prefix}graph osu_username pp 7      description: Shows last 7 day's pp line chart\n"
        output += f"{prefix}graph osu_username rank      description: Shows a rank line chart with all data we have\n\n"
        output += "Description: Available line charts 'pp', 'rank', 'acc', 'pc', 'countryrank'\n"
        output += "instead of osu_username u can mention linked users or you just dont give any username for self use\n"
        output += f"Examples: {prefix}{command_name} @discord_user or {prefix}{command_name}"

    elif command_name == "invite":
        output += "Gives you a nice invite link\n"
        output += "Example Usage\n\n"
        output += f"{prefix}invite"

    else:
        return await ctx.send(f"Invalid Command Name Type {prefix}help for command list")

    output += "```"
    await ctx.send(output)
