import random


def get_roll_text(num):
    try:
        output = random.randint(1, int(num))
    except:
        output = random.randint(1, 100)
    return output