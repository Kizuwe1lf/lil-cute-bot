import requests
import json
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from scripts import *
from discord import File
import os


async def write_to_image(ctx, scores, get_beatmaps, comm_name):
    score_count = 8
    if len(scores) < 8:
        score_count = len(scores)
        if len(scores) == 0:
            await ctx.send("There are no scores <:aquaCry:700623201880899604>")
            return 0

    height = 255 + (score_count * 110)
    width = 1200
    rank_area = (111, 14)
    score_area = (177, 50)
    pp_area = (700, 50)
    mod_area= (940, 50)

    nick_area = (177, 6)
    date_time_area = (940, 6)
    accuracy_area = (700, 6)
    font_colour = (255, 255, 255)
    mod_font_colour = (0, 255, 255)
    font = ImageFont.truetype("my_files/global_materials/font.ttf", 44)

    title_font = ImageFont.truetype("my_files/global_materials/font.ttf", 50)

    header = Image.open('my_files/global_materials/header.png')
    draw = ImageDraw.Draw(header)
    draw.text((15, 10), f"{get_beatmaps[0]['title']}", font_colour, font=title_font)
    draw.text((15, 80), f"[{get_beatmaps[0]['version']}]", font_colour, font=title_font)


    img = Image.new(mode='RGBA', size= (width, height))
    img.paste(header, (0, 0))

    i = 0
    while i < score_count: # Writing Score Variables in this loop

        mods_list = num_to_mod_list(scores[i]['enabled_mods'])
        mods_text = ''.join(mods_list)

        count = [scores[i]['countmiss'], scores[i]['count50'], scores[i]['count100'], scores[i]['count300']]
        accuracy_text = round_func(calc_accuracy(*count))

        score_date = datetime.strptime(scores[i]['date'], '%Y-%m-%d %H:%M:%S')
        score_date = score_date.strftime('%m-%d-%Y')

        misstext = ""
        if int(scores[i]['countmiss']) > 0:
            misstext = f"{scores[i]['countmiss']}x"
        score_text_ = get_score(scores[i]['score'])
        score = Image.open('my_files/global_materials/middle.png')
        draw = ImageDraw.Draw(score)
        draw.text(nick_area, f"{scores[i]['username']}", font_colour, font=font)
        draw.text(score_area, f"{score_text_} ({scores[i]['maxcombo']}x) {misstext}", font_colour, font=font)
        draw.text(mod_area, f"{mods_text}", mod_font_colour, font=font)

        if scores[i]['pp'] is not None:
            pp_text = round_func(scores[i]['pp'])
        else:
            pp_text = get_pp(get_beatmaps[0]['beatmap_id'], mods_list, scores[i]['maxcombo'], count)['pp']

        draw.text(pp_area, f"{pp_text}pp", font_colour, font=font)
        draw.text(date_time_area, f"{score_date}", font_colour, font=font)
        draw.text(accuracy_area, f"{accuracy_text}%", font_colour, font=font)


        rank = Image.open(f"my_files/global_materials/{scores[i]['rank']}.png")
        score.paste(rank, rank_area, rank)

        avatar = get_user_avatar(scores[i]['user_id'])
        position = 155 + ( i * 110 )
        img.paste(avatar, (13, position + 8))
        img.paste(score, (0, position), score)
        i += 1


    footer = Image.open('my_files/global_materials/footer.png')
    draw = ImageDraw.Draw(footer)
    draw.text((15, 23), f"Beatmap by {get_beatmaps[0]['creator']}", font_colour, font=title_font)
    img.paste(footer, (0, position + 110))
    img_path = f'my_files/{comm_name}{ctx.channel.id}.png'
    img.save(img_path)
    await ctx.send(file=File(img_path))
    os.remove(img_path)
