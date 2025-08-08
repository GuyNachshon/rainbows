import requests
import os
import json
import datetime
from tqdm import tqdm
from multiprocessing import Pool

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, 'data')
SAMPLE_VIDEOS_PATH = os.path.join(DATA_DIR, 'sample_videos.json')
OUTPUT_PATH = os.path.join(DATA_DIR, 'videos_with_m3u8.json')

# From collect_items.py
CHANNELS = {
    "35e7ec884d0fc610VgnVCM200000650a10acRCRD": {
        "channelName": "המהדורה המרכזית",
    },
    "4064b3866ebfc610VgnVCM100000700a10acRCRD": {
        "channelName": "חדשות סוף השבוע",
    },
    "17d45d19cebfc610VgnVCM100000700a10acRCRD": {
        "channelName": "אולפן שישי",
    },
    "75f651b92fbfc610VgnVCM100000700a10acRCRD": {
        "channelName": "שש עם עודד בן עמי",
    },
    "3c07e8468fbfc610VgnVCM100000700a10acRCRD": {
        "channelName": "מהדורה ראשונה",
    },
    "91ea5bf310cfc610VgnVCM100000700a10acRCRD": {
        "channelName": "סדר עולמי",
    },
    "e90cdc0540cfc610VgnVCM100000700a10acRCRD": {
        "channelName": "המהדורה הצעירה",
    },
    "1a03dc0540cfc610VgnVCM100000700a10acRCRD": {
        "channelName": "תוכנית חיסכון",
    },
    "b96281b1c0cfc610VgnVCM100000700a10acRCRD": {
        "channelName": "השבוע בערבית",
    },
    "f595719af0cfc610VgnVCM100000700a10acRCRD": {
        "channelName": "מבזקי חדשות 12",
    },
    "bdb5acc8b2cfc610VgnVCM100000700a10acRCRD": {
        "channelName": "חמש עם רפי רשף",
    },
    "5445fcf6e2cfc610VgnVCM100000700a10acRCRD": {
        "channelName": "פגוש את העיתונות",
    },
    "d0dd36f3de6ae610VgnVCM200000650a10acRCRD": {
        "channelName": "המהדורות המלאות",
    },
    "2d68775b26694710VgnVCM200000650a10acRCRD": {
        "channelName": "מהדורת היום",
    },
    "d4b93d69104f4710VgnVCM200000650a10acRCRD": {
        "channelName": "שבת בחמש",
    },
    "e976e23f9b6b4910VgnVCM100000700a10acRCRD": {
        "channelName": "משדר 12",
    }
}

CHANNEL_NAME_TO_PREFIX = {
    "אולפן שישי": "ulpash",
    "המהדורה המרכזית": "20mahadurafull",
    "לא ידוע": "",  # Add a fallback for unknown channels
    # Add more mappings here
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "priority": "u=0, i",
    "sec-ch-ua": "\"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"138\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"macOS\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1"
}


def generate_m3u8_url(video):
    date_obj = datetime.datetime.strptime(video['date'], '%d.%m.%Y')
    year = date_obj.strftime('%Y')
    month = date_obj.strftime('%m')
    date_str = date_obj.strftime('%Y%m%d')

    video_name = video.get('videoName', '')

    prefix = None
    if "אולפן שישי" in video_name:
        prefix = "ulpash"
    elif "המהדורה המרכזית" in video_name:
        prefix = "20mahadurafull"

    if not prefix:
        channel_name = video.get('channelName')
        if channel_name and channel_name in CHANNEL_NAME_TO_PREFIX:
            prefix = CHANNEL_NAME_TO_PREFIX[channel_name]

    if not prefix:
        return None

    asset_name = f"{prefix}_vtr2_n{date_str}_v1"

    # URL Pattern 1
    url1 = f"https://mako-vod.akamaized.net/i/SHORT/CH22_NEWS/{year}/{month}/{asset_name}/{asset_name}_,850,.mp4.csmil/master.m3u8"
    try:
        if requests.head(url1, timeout=2).status_code == 200:
            return url1
    except requests.RequestException:
        pass

    # URL Pattern 2
    url2 = f"https://mako-vod.akamaized.net/i/SHORT/CH22_NEWS/{year}/{month}/{asset_name}/850/index_850.m3u8"
    try:
        if requests.head(url2, timeout=2).status_code == 200:
            return url2
    except requests.RequestException:
        pass

    return None


def main():
    with open(SAMPLE_VIDEOS_PATH, 'r', encoding='utf-8') as f:
        videos = json.load(f)

    with Pool() as pool:
        results = list(tqdm(pool.imap(generate_m3u8_url, videos), total=len(videos), desc="Generating M3U8 URLs"))

    videos_with_m3u8 = []
    for i, m3u8_url in enumerate(results):
        if m3u8_url:
            video = videos[i]
            video['m3u8_url'] = m3u8_url
            videos_with_m3u8.append(video)

    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(videos_with_m3u8, f, ensure_ascii=False, indent=4)

    print(f"Successfully found M3U8 URLs for {len(videos_with_m3u8)} of {len(videos)} videos.")


if __name__ == "__main__":
    main()
