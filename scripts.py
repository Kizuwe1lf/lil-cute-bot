import asyncio
import database
from downloader import *


class Beatmaps:
    def __init__(self, beatmap_id, mods=0):
        self.bmap = download_beatmaps(beatmap_id)
        self.stars = osu.diff_calc().calc(self.bmap, int(mods))
        self.mods = mods

    def get_mapcompletion(self, totalhits=0): # obj = object
        hitobj = []
        if totalhits == 0:
            totalhits = len(self.bmap.hitobjects)
        numobj = totalhits - 1
        num = len(self.bmap.hitobjects)
        for objects in self.bmap.hitobjects:
            hitobj.append(objects.time)
        timing = int(hitobj[num - 1]) - int(hitobj[0])
        point = int(hitobj[numobj]) - int(hitobj[0])
        map_completion = (point / timing) * 100
        return round(map_completion, 2)

    def get_if_fc_pp(self, acc):
        aim = self.stars.aim
        speed = self.stars.speed
        n300, n100, n50 = osu.acc_round(acc, len(self.bmap.hitobjects), 0)
        pp, aim_pp, speed_pp, acc_pp, accuraccy = osu.ppv2(
            aim_stars=aim, speed_stars=speed,
            n300=n300,
            n50=n50,
            n100=n100,
            nmiss=0,
            bmap=self.bmap, mods=self.mods, combo=self.bmap.max_combo())
        output = f"IF FC: **{int(round(pp))}**pp |"
        return output

    def get_pp(self, maxcombo, miss, n50, n100, n300):
        aim = self.stars.aim
        speed = self.stars.speed
        pp, aim_pp, speed_pp, acc_pp, accuraccy = osu.ppv2(
            aim_stars=aim, speed_stars=speed,
            n300=int(n300),
            n50=int(n50),
            n100=int(n100),
            nmiss=int(miss),
            bmap=self.bmap, mods=self.mods, combo=maxcombo)
        output = f"**{int(round(pp))}**pp |"
        return output

    def get_stars(self):
        return round(self.stars.total, 2)

    def get_beatmap_data(self):
        bmap = self.bmap
        data = [bmap.cs, bmap.ar, bmap.od, bmap.hp]
        return data

    def get_accuracy_pps(self):
        pp_list = []
        acc_list = [95, 98, 99, 100]
        for x in range(4):
            aim = self.stars.aim
            speed = self.stars.speed
            n300, n100, n50 = osu.acc_round(acc_list[x], len(self.bmap.hitobjects), 0)
            pp, aim_pp, speed_pp, acc_pp, accuraccy = osu.ppv2(
                aim_stars=aim, speed_stars=speed,
                n300=n300,
                n50=n50,
                n100=n100,
                nmiss=0,
                bmap=self.bmap, mods=self.mods, combo=self.bmap.max_combo())

            pp_list.append(round(pp, 2))
        return pp_list


def acc_calculator(x, y, z, c): # x,y,z,c  miss 50 100 300 
    total_score = float(y)
    total_score += float(z)
    total_score += float(c)
    total_score += float(x)
    total_score *= 300
    user_score = float(y) * 50
    user_score += float(z) * 100
    user_score += float(c) * 300
    return float(user_score) * 100 / float(total_score)


def no_choke_acc(x, y, z, c): # x,y,z,c  miss 50 100 300 
    total_score = float(y)
    total_score += float(z)
    total_score += float(c)
    total_score += float(x)
    total_score *= 300
    user_score = float(y) * 50
    user_score += float(z) * 100
    user_score += float(c) * 300
    user_score += float(x) * 100
    return float(user_score) * 100 / float(total_score)


def num_to_mod(number):
    mod_list = []
    number = int(number)
    if number == 0:
        mod_list.append('No Mod,')
        return ''.join(mod_list)
    if   number & 1 << 0:   mod_list.append('NF')
    if   number & 1 << 1:   mod_list.append('EZ')
    if   number & 1 << 2:   mod_list.append('TD')
    if   number & 1 << 3:   mod_list.append('HD')
    if   number & 1 << 4:   mod_list.append('HR')
    if   number & 1 << 5:   mod_list.append('SD')
    if   number & 1 << 9:   
        mod_list.append('NC')
    elif number & 1 << 6:   
        mod_list.append('DT')
    if   number & 1 << 7:   mod_list.append('RX')
    if   number & 1 << 8:   mod_list.append('HT')
    if   number & 1 << 10:  mod_list.append('FL')
    if   number & 1 << 12:  mod_list.append('SO')
    if   number & 1 << 14:  mod_list.append('PF')
    if   number & 1 << 20:  mod_list.append('FI')
    if   number & 1 << 29:  mod_list.append('v2')
    return ''.join(mod_list)

def num_to_mod_image(number):
    mod_list = []
    number = int(number)
    if number == 0:
        mod_list.append('No Mod,')
        return ''.join(mod_list)
    if   number & 1 << 0:   mod_list.append('NF,')
    if   number & 1 << 1:   mod_list.append('EZ,')
    if   number & 1 << 2:   mod_list.append('TD,')
    if   number & 1 << 3:   mod_list.append('HD,')
    if   number & 1 << 4:   mod_list.append('HR,')
    if   number & 1 << 5:   mod_list.append('SD,')
    if   number & 1 << 12:  mod_list.append('SO,')
    if   number & (( 1 << 9 ) + ( 1 << 6 )) == 576:   
        mod_list.append('NC,')
    elif number & (( 1 << 9 ) + ( 1 << 6 )) == 64:
        mod_list.append('DT,')
    if   number & 1 << 7:   mod_list.append('RX,')
    if   number & 1 << 8:   mod_list.append('HT,')
    if   number & 1 << 10:  mod_list.append('FL,')
    if   number & 1 << 12:  mod_list.append('SO,')
    if   number & 1 << 14:  mod_list.append('PF,')
    if   number & 1 << 20:  mod_list.append('FI,')
    if   number & 1 << 29:  mod_list.append('v2,')
    return ''.join(mod_list)
    
def mod_to_num(mods: str):
    mods = mods.upper()
    total = 0
    if   'NF' in mods:    total += 1 << 0
    if   'EZ' in mods:    total += 1 << 1
    if   'TD' in mods:    total += 1 << 2
    if   'HD' in mods:    total += 1 << 3
    if   'HR' in mods:    total += 1 << 4
    if   'SD' in mods:    total += 1 << 5
    if   'NC' in mods:
        total += (( 1 << 9 ) + ( 1 << 6 ))
    elif 'DT' in mods:
        total += 1 << 6
    if   'RX' in mods:    total += 1 << 7
    if   'HT' in mods:    total += 1 << 8
    if   'FL' in mods:    total += 1 << 10
    if   'SO' in mods:    total += 1 << 12
    if   'PF' in mods:    total += 1 << 14
    if   'FI' in mods:    total += 1 << 20
    if   'v2' in mods:    total += 1 << 29
       
    return int(total) 


def get_fifty_emote():
    return f"<:50_Emote:649799152519086082>"


def get_onehundred_emote():
    return f"<:100_Emote:649794377954230283>"


def get_miss_emote():
    return f"<:Miss_Emote:649801261046038528>"


def get_rank_emote(rank):
    if rank == "A":
        return "<:A_Emote:649752233226928131>"
    if rank == "B":
        return "<:B_Emote:649752243259703317>"
    if rank == "C":
        return "<:C_Emote:649752253883744265>"
    if rank == "D":
        return "<:D_Emote:649752265095380993>"
    if rank == "XH":  # SS hidden
        return "<:SSH_Emote:649752313677873184>"
    if rank == "SH":  # S Hidden
        return "<:SH_Emote:649752294665093140>"
    if rank == "X":  # SS
        return "<:SS_Emote:649752304357998632>"
    if rank == "S":
        return "<:S_Emote:649752285613785121>"
    if rank == "F":
        return "<:F_Emote:649752275694125056>"

    return rank


def get_beatmap_image_url(beatmap_id):
    return f"https://b.ppy.sh/thumb/{beatmap_id}l.jpg"


def time_ago(play_time, base_time):
    totalseconds = (base_time - play_time).total_seconds()
    total_minutes = totalseconds / 60
    total_hours = total_minutes / 60
    total_days = total_hours / 24
    total_months = total_days / 30
    total_years = total_months / 12

    if totalseconds <= 30:
        return "Submitted **Just Now**"
    elif totalseconds < 60:
        return f"**{int(totalseconds)} seconds** ago"
    elif total_minutes < 60:
        return f"**{int(total_minutes)} minutes** ago"
    elif total_hours < 24:
        return f"**{int(total_hours)} hours** ago"
    elif total_days < 30:
        return f"**{int(total_days)} days** ago"
    elif total_months < 12:
        if total_days - int(total_months) * 30 >= 5:
            return f"**{int(total_months)} months {int(total_days - int(total_months) * 30)} days** ago"
        else:
            return f"**{int(total_months)} months** ago"
    else:
        if total_months - int(total_years) * 12 >= 1:
            return f"**{int(total_years)} years {int(total_months - int(total_years) * 12)} months** ago"
        else:
            return f"**{int(total_years)} years** ago"

def get_score(score):
    stringscore = str(score)
    score = ""
    counter = 3 - (len(stringscore) % 3)
    i = 0
    while i < len(stringscore):
        score += stringscore[i]
        counter += 1
        if counter % 3 == 0:
            score += ","
        i += 1
    return score[:-1]


def get_total_hours_played(seconds):
    return int(round(int(seconds) / 60 / 60))


async def send_pages(ctx, e, info, total_pages, bot):
    cur_page = 1
    left = "<:slide_left:734860817584881674>"
    right = "<:slide_right:734860832642433164>"
    e.description = info[cur_page-1]
    e.set_footer(text=f"Pages {cur_page} out of {total_pages}")
    message = await ctx.send(embed=e)
    await message.add_reaction(right)

    def check(r, u):
        return u == ctx.message.author and str(r.message) == str(message) and (str(r.emoji) == left or str(r.emoji) == right)

    while True:
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
            if str(reaction.emoji) == right:
                await message.clear_reaction(right)
                await message.clear_reaction(left)
                cur_page += 1
                e.description = info[cur_page - 1]
                e.set_footer(text=f"Pages {cur_page} out of {total_pages}")
                await message.edit(embed=e)
                await message.add_reaction(left)
                if cur_page != total_pages:
                    await message.add_reaction(right)

            elif str(reaction.emoji) == left:
                await message.clear_reaction(right)
                await message.clear_reaction(left)
                cur_page -= 1
                e.description = info[cur_page - 1]
                e.set_footer(text=f"Pages {cur_page} out of {total_pages}")
                await message.edit(content=None, embed=e)
                if cur_page != 1:
                    await message.add_reaction(left)
                await message.add_reaction(right)
        except asyncio.TimeoutError:
            break
