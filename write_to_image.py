import requests
import json
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from scripts import *
from bot_commands.c_main import stuff


def write_to_image(scores, get_beatmaps):
    score_count = 8
    if len(scores) < 8:
        score_count = len(scores)
        if len(scores) == 0:
            return "There are no scores :("
            
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
        
        
        mod_text = str(num_to_mod_image(scores[i]['enabled_mods']))
        mod_text = mod_text[:-1]
        
        count = [scores[i]['countmiss'], scores[i]['count50'], scores[i]['count100'], scores[i]['count300']]
        accuracy_text = acc_calculator(*count)
        
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
        draw.text(mod_area, f"{mod_text}", mod_font_colour, font=font)
        try:
            draw.text(pp_area, f"{float(scores[i]['pp']):0.2f}pp", font_colour, font=font)
        except:
            accuracy_area = pp_area
        draw.text(date_time_area, f"{score_date}", font_colour, font=font)
        draw.text(accuracy_area, f"{accuracy_text:0.2f}%", font_colour, font=font)
        

        rank = Image.open(f"my_files/global_materials/{scores[i]['rank']}.png")
        score.paste(rank, rank_area, rank)
        
        avatar = download_avatar(scores[i]['user_id'])
        position = 155 + ( i * 110 )
        img.paste(avatar, (13, position + 8))
        img.paste(score, (0, position), score) 
        i += 1


    footer = Image.open('my_files/global_materials/footer.png')
    draw = ImageDraw.Draw(footer)
    draw.text((15, 23), f"Beatmap by {get_beatmaps[0]['creator']}", font_colour, font=title_font)
    img.paste(footer, (0, position + 110))
    img.save('my_files/global_materials/output.png')
    return 'my_files/global_materials/output.png'
