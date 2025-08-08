import json
import os
import requests
from tqdm import tqdm
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, 'data')
LONG_VIDEOS_PATH = os.path.join(DATA_DIR, 'long_videos.json')
OUTPUT_PATH = os.path.join(DATA_DIR, 'videos_with_m3u8.json')


def get_player_guid(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        match = re.search(r'guid=([a-zA-Z0-9]+)', response.text)
        if match:
            return match.group(1)
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
    return None


def build_m3u8_url_from_guid(guid):
    return f"https://mako-vod.akamaized.net/i/mako-vod-tb/2024/01/01/{guid}/,index_850.m3u8.csmil/index_850.m3u8"


def main():
    with open(LONG_VIDEOS_PATH, 'r', encoding='utf-8') as f:
        videos = json.load(f)

    videos_with_m3u8 = []
    for video in tqdm(videos, desc="Processing videos"):
        video_page_url = f"https://www.mako.co.il{video['videoLink']}"
        guid = get_player_guid(video_page_url)
        if guid:
            m3u8_url = build_m3u8_url_from_guid(guid)
            video['m3u8_url'] = m3u8_url
            videos_with_m3u8.append(video)

    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(videos_with_m3u8, f, ensure_ascii=False, indent=4)

    print(f"Successfully processed {len(videos_with_m3u8)} videos.")


if __name__ == "__main__":
    main()
