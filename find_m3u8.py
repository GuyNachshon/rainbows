import requests
import os
import json
import datetime
from tqdm import tqdm

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, 'data')
LONG_VIDEOS_PATH = os.path.join(DATA_DIR, 'sample_videos.json')
OUTPUT_PATH = os.path.join(DATA_DIR, 'videos_with_m3u8.json')


def get_m3u8_url(video):
    date_str = datetime.datetime.strptime(video['date'], '%d.%m.%Y').strftime('%Y%m%d')
    year = date_str[:4]
    month = date_str[4:6]

    # Pattern 1: From collect_m3u8.py
    url1 = f"https://mako-vod.akamaized.net/i/SHORT/CH22_NEWS/{year}/{month}/20mahadurafull_vtr2_n{date_str}_v1/850/index_850.m3u8"
    print(f"Checking URL: {url1}")
    if requests.head(url1).status_code == 200:
        return url1

    # Add more patterns here as we discover them

    return None


def main():
    with open(LONG_VIDEOS_PATH, 'r', encoding='utf-8') as f:
        videos = json.load(f)

    videos_with_m3u8 = []
    for video in tqdm(videos, desc="Finding M3U8 URLs"):
        m3u8_url = get_m3u8_url(video)
        if m3u8_url:
            video['m3u8_url'] = m3u8_url
            videos_with_m3u8.append(video)

    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(videos_with_m3u8, f, ensure_ascii=False, indent=4)

    print(f"Successfully found M3U8 URLs for {len(videos_with_m3u8)} videos.")


if __name__ == "__main__":
    main()
