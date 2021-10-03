import urllib.request
import os.path
from os import path
import numpy
import requests
from PIL import Image


def get_beatmap_path(beatmap_id):
    pathname = f'my_files/beatmap_folder/{beatmap_id}.osu'
    if path.exists(pathname) is False:
        return download_beatmaps(beatmap_id, pathname)
    else:
        return pathname

def download_beatmaps(beatmap_id, pathname):
    url = f"https://osu.ppy.sh/osu/{beatmap_id}"
    urllib.request.urlretrieve(url, pathname)
    return pathname

def get_avg_colour_from_cover(beatmapset_id):
    pathname = f'my_files/beatmap_covers/{beatmapset_id}.jpg'
    if path.exists(pathname) is False:
        download_thumbnails(beatmapset_id, pathname)
    try:
        with Image.open(pathname) as i:
            avg_color_per_row = numpy.average(i, axis=0)
            dominant_color = numpy.average(avg_color_per_row, axis=0) # getting avg colour data as float RGB
        dominant_color = list(map(round, dominant_color)) # converting to int
        return dominant_color
    except:
        return [1, 1, 1] # return black if theres a problem (some beatmap covers has lil bugs)

def download_thumbnails(beatmapset_id, pathname):
    url = f'https://assets.ppy.sh/beatmaps/{beatmapset_id}/covers/cover.jpg'
    r = requests.get(url, allow_redirects=True)
    open(pathname, 'wb').write(r.content)


def get_user_avatar(user_id):
    pathname = f'my_files/user_avatars/{user_id}.png'
    if path.exists(pathname) is False:
        download_avatar(user_id, pathname)

    avatar = Image.open(pathname)
    avatar = avatar.resize((94, 94)) # resizing avatar i need 94x94
    avatar.save(pathname)

    return avatar

def download_avatar(user_id, pathname):
    url = f'https://a.ppy.sh/{user_id}'
    r = requests.get(url, allow_redirects=True)
    open(pathname, 'wb').write(r.content)

def get_beatmap_thumb_url(beatmap_id): # i dont need to download this
    return f"https://b.ppy.sh/thumb/{beatmap_id}l.jpg"
