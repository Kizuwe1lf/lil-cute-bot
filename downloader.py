import urllib.request
import os.path
from os import path
import numpy
import pyttanko as osu
import requests
from PIL import Image


def get_average_color_from_image(image):
    with Image.open(image) as i:
        avg_color_per_row = numpy.average(i, axis=0)
        return numpy.average(avg_color_per_row, axis=0)


def download_beatmaps(beatmapset_id):
    url = f"https://osu.ppy.sh/osu/{beatmapset_id}"
    pathname = 'beatmap_folder/'
    pathname += url.split("/")[-1]
    if path.exists(pathname) is False:
        urllib.request.urlretrieve(url, pathname)
    p = osu.parser()
    osu_map_path = os.path.join(pathname)
    with open(osu_map_path, "r", encoding="utf-8") as f:
        uwu = p.map(f)
    return uwu


def download_thumbnails(beatmapset_id):
    url = f'https://assets.ppy.sh/beatmaps/{beatmapset_id}/covers/cover.jpg'
    pathname = f'beatmap_covers/{beatmapset_id}.jpg'
    r_g_b = [1, 1, 1]
    if path.exists(pathname) is False:
        r = requests.get(url, allow_redirects=True)
        open(pathname, 'wb').write(r.content)
    try:
        dominant_color = get_average_color_from_image(pathname)
        for x in range(3):
            r_g_b[x] = int(dominant_color[x])
    except:
        pass
    return r_g_b
    
def download_avatar(user_id):
    url = f'https://a.ppy.sh/{user_id}'
    pathname = f'my_files/user_avatars/{user_id}.png'
    if path.exists(pathname) is False:
        r = requests.get(url, allow_redirects=True)
        open(pathname, 'wb').write(r.content)
        resize_avatar(pathname)
    avatar = Image.open(pathname)
    return avatar


def resize_avatar(pathname):
    avatar = Image.open(pathname)
    avatar = avatar.resize((94, 94))
    avatar.save(pathname)
