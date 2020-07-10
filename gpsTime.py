from datetime import datetime
from gwpy.time import tconvert, to_gps

def cleander_to_gps(year, month, day, hour, minute, second):
    time = datetime(year, month, day, hour, minute, second)
    all_seconds = to_gps(time) - 18
    week = int(all_seconds/604800)
    second = all_seconds % 604800
    return (week, second)


def gps_to_cleander(week, second):
    all_seconds = week * 604800 + second + 18
    return tconvert(all_seconds)
