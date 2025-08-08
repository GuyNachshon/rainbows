import requests
import os
import json
import datetime
from tqdm import tqdm
import xml.etree.ElementTree as ET

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, 'data')
LONG_VIDEOS_PATH = os.path.join(DATA_DIR, 'long_videos.json')
OUTPUT_PATH = os.path.join(DATA_DIR, 'videos_with_m3u8.json')

CONFIG_URL_TEMPLATE = "https://www.mako.co.il/VodPlayer/player_config.ashx?guid={guid}"


def get_m3u8_from_config(guid):
    config_url = CONFIG_URL_TEMPLATE.format(guid=guid)
    try:
        response = requests.get(config_url)
        response.raise_for_status()
        root = ET.fromstring(response.content)
        m3u8_url_element = root.find('.//PlayerProperties[@protocol="HLS"]/URL')
        if m3u8_url_element is not None:
            return m3u8_url_element.text
    except requests.RequestException as e:
        print(f"Error fetching config for {guid}: {e}")
    except ET.ParseError as e:
        print(f"Error parsing XML for {guid}: {e}")
    return None

def main():
    with open(LONG_VIDEOS_PATH, 'r', encoding='utf-8') as f:
        videos = json.load(f)

    videos_with_m3u8 = []
    for video in tqdm(videos, desc="Processing videos"):
        guid = video.get('videoId')
        if guid:
            m3u8_url = get_m3u8_from_config(guid)
            if m3u8_url:
                video['m3u8_url'] = m3u8_url
                videos_with_m3u8.append(video)

    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(videos_with_m3u8, f, ensure_ascii=False, indent=4)

    print(f"Successfully processed {len(videos_with_m3u8)} videos.")

if __name__ == "__main__":
    main()
