import datetime
import json
from threading import Lock
import requests
from tqdm import tqdm
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, 'data')
FILE_PATH = os.path.join(DATA_DIR, 'videos.json')
FILE_PATH_VERSION = os.path.join(DATA_DIR, 'videos.json.version')
INITIAL_DATE = datetime.datetime(2023, 10, 7)
VERSION = None
BASE_URL = "https://www.mako.co.il/AjaxPage?jspName=videoGalleryChannelPageResponse.jsp&galleryChannelId=e30cc13e751fc610VgnVCM200000650a10acRCRD"
CHANNELS = {
    "35e7ec884d0fc610VgnVCM200000650a10acRCRD": {
        "channelName": "המהדורה המרכזית",
        "referring_component": "3752456d-glry-chnl-refc-f3fe0116cd38",
        "channelId": "35e7ec884d0fc610VgnVCM200000650a10acRCRD",
        "channelLink": "/news-channel12?subChannelId=35e7ec884d0fc610VgnVCM200000650a10acRCRD"
    },
    "4064b3866ebfc610VgnVCM100000700a10acRCRD": {
        "channelName": "חדשות סוף השבוע",
        "referring_component": "3752456d-glry-chnl-refc-f3fe0116cd38",
        "channelId": "4064b3866ebfc610VgnVCM100000700a10acRCRD",
        "channelLink": "/news-channel12?subChannelId=4064b3866ebfc610VgnVCM100000700a10acRCRD"
    },
    "17d45d19cebfc610VgnVCM100000700a10acRCRD": {
        "channelName": "אולפן שישי",
        "referring_component": "3752456d-glry-chnl-refc-f3fe0116cd38",
        "channelId": "17d45d19cebfc610VgnVCM100000700a10acRCRD",
        "channelLink": "/news-channel12?subChannelId=17d45d19cebfc610VgnVCM100000700a10acRCRD"
    },
    "75f651b92fbfc610VgnVCM100000700a10acRCRD": {
        "channelName": "שש עם עודד בן עמי",
        "referring_component": "3752456d-glry-chnl-refc-f3fe0116cd38",
        "channelId": "75f651b92fbfc610VgnVCM100000700a10acRCRD",
        "channelLink": "/news-channel12?subChannelId=75f651b92fbfc610VgnVCM100000700a10acRCRD"
    },
    "3c07e8468fbfc610VgnVCM100000700a10acRCRD": {
        "channelName": "מהדורה ראשונה",
        "referring_component": "3752456d-glry-chnl-refc-f3fe0116cd38",
        "channelId": "3c07e8468fbfc610VgnVCM100000700a10acRCRD",
        "channelLink": "/news-channel12?subChannelId=3c07e8468fbfc610VgnVCM100000700a10acRCRD"
    },
    "91ea5bf310cfc610VgnVCM100000700a10acRCRD": {
        "channelName": "סדר עולמי",
        "referring_component": "3752456d-glry-chnl-refc-f3fe0116cd38",
        "channelId": "91ea5bf310cfc610VgnVCM100000700a10acRCRD",
        "channelLink": "/news-channel12?subChannelId=91ea5bf310cfc610VgnVCM100000700a10acRCRD"
    },
    "e90cdc0540cfc610VgnVCM100000700a10acRCRD": {
        "channelName": "המהדורה הצעירה",
        "referring_component": "3752456d-glry-chnl-refc-f3fe0116cd38",
        "channelId": "e90cdc0540cfc610VgnVCM100000700a10acRCRD",
        "channelLink": "/news-channel12?subChannelId=e90cdc0540cfc610VgnVCM100000700a10acRCRD"
    },
    "1a03dc0540cfc610VgnVCM100000700a10acRCRD": {
        "channelName": "תוכנית חיסכון",
        "referring_component": "3752456d-glry-chnl-refc-f3fe0116cd38",
        "channelId": "1a03dc0540cfc610VgnVCM100000700a10acRCRD",
        "channelLink": "/news-channel12?subChannelId=1a03dc0540cfc610VgnVCM100000700a10acRCRD"
    },
    "b96281b1c0cfc610VgnVCM100000700a10acRCRD": {
        "channelName": "השבוע בערבית",
        "referring_component": "3752456d-glry-chnl-refc-f3fe0116cd38",
        "channelId": "b96281b1c0cfc610VgnVCM100000700a10acRCRD",
        "channelLink": "/news-channel12?subChannelId=b96281b1c0cfc610VgnVCM100000700a10acRCRD"
    },
    "f595719af0cfc610VgnVCM100000700a10acRCRD": {
        "channelName": "מבזקי חדשות 12",
        "referring_component": "3752456d-glry-chnl-refc-f3fe0116cd38",
        "channelId": "f595719af0cfc610VgnVCM100000700a10acRCRD",
        "channelLink": "/news-channel12?subChannelId=f595719af0cfc610VgnVCM100000700a10acRCRD"
    },
    "bdb5acc8b2cfc610VgnVCM100000700a10acRCRD": {
        "channelName": "חמש עם רפי רשף",
        "referring_component": "3752456d-glry-chnl-refc-f3fe0116cd38",
        "channelId": "bdb5acc8b2cfc610VgnVCM100000700a10acRCRD",
        "channelLink": "/news-channel12?subChannelId=bdb5acc8b2cfc610VgnVCM100000700a10acRCRD"
    },
    "5445fcf6e2cfc610VgnVCM100000700a10acRCRD": {
        "channelName": "פגוש את העיתונות",
        "referring_component": "3752456d-glry-chnl-refc-f3fe0116cd38",
        "channelId": "5445fcf6e2cfc610VgnVCM100000700a10acRCRD",
        "channelLink": "/news-channel12?subChannelId=5445fcf6e2cfc610VgnVCM100000700a10acRCRD"
    },
    "d0dd36f3de6ae610VgnVCM200000650a10acRCRD": {
        "channelName": "המהדורות המלאות",
        "referring_component": "3752456d-glry-chnl-refc-f3fe0116cd38",
        "channelId": "d0dd36f3de6ae610VgnVCM200000650a10acRCRD",
        "channelLink": "/news-channel12?subChannelId=d0dd36f3de6ae610VgnVCM200000650a10acRCRD"
    },
    "2d68775b26694710VgnVCM200000650a10acRCRD": {
        "channelName": "מהדורת היום",
        "referring_component": "3752456d-glry-chnl-refc-f3fe0116cd38",
        "channelId": "2d68775b26694710VgnVCM200000650a10acRCRD",
        "channelLink": "/news-channel12?subChannelId=2d68775b26694710VgnVCM200000650a10acRCRD"
    },
    "d4b93d69104f4710VgnVCM200000650a10acRCRD": {
        "channelName": "שבת בחמש",
        "referring_component": "3752456d-glry-chnl-refc-f3fe0116cd38",
        "channelId": "d4b93d69104f4710VgnVCM200000650a10acRCRD",
        "channelLink": "/news-channel12?subChannelId=d4b93d69104f4710VgnVCM200000650a10acRCRD"
    },
    "e976e23f9b6b4910VgnVCM100000700a10acRCRD": {
        "channelName": "משדר 12",
        "referring_component": "3752456d-glry-chnl-refc-f3fe0116cd38",
        "channelId": "e976e23f9b6b4910VgnVCM100000700a10acRCRD",
        "channelLink": "/news-channel12?subChannelId=e976e23f9b6b4910VgnVCM100000700a10acRCRD"
    }
}
VERSION_LOCK = Lock()

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


def get_version():
    global VERSION
    if VERSION is None:
        try:
            with open(FILE_PATH_VERSION, 'r') as f:
                VERSION = f.read().strip()
        except FileNotFoundError:
            VERSION = None
    return VERSION


def save_version(version):
    global VERSION
    VERSION = version
    with VERSION_LOCK:
        with open(FILE_PATH_VERSION, 'w+') as f:
            f.write(str(version))


def _fetch_videos_page(p=1):
    _url = f"{BASE_URL}&page={p}"
    try:
        response = requests.get(_url, headers=headers, timeout=100)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching page {p}: {e}")
        return None


def normalize_video(item):
    if isinstance(item, str):
        item = json.loads(item)
    _date = datetime.datetime.strptime(item.get("videoDate"), "%d.%m.%y")
    duration = item.get("videoDuration")
    video_name = item.get("videoName")
    description = item.get("description")
    video_id = item.get("videoId")
    video_link = item.get("videoLink")
    channel = item.get("channelId")
    channel_name = CHANNELS.get(channel, {}).get("channelName", "לא ידוע")
    return {
        "date": _date,
        "duration": duration,
        "videoName": video_name,
        "description": description,
        "videoId": video_id,
        "videoLink": video_link,
        "channelId": channel,
        "channelName": channel_name
    }


def fetch_videos():
    p = 1
    while True:
        if p < int(get_version()):
            print(f"Skipping page {p} as it is already processed.")
            p += 1
            continue
        items = _fetch_videos_page(p=p)
        videos = []
        if not items:
            print(f"No items found on page {p}. Stopping.")
            break
        for item in tqdm(items.get("videos", []), desc=f"Fetching videos page {p}"):
            video = normalize_video(item)
            if video.get("date") < INITIAL_DATE:
                break
            video["date"] = video["date"].strftime("%d.%m.%Y")
            videos.append(video)
            save_version(p)
        if not videos:
            break
        yield videos
        p += 1


def analyze_videos():
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        all_videos = json.load(f)
    relevant_videos = []
    minimal_length = 15 * 60  # 15 minutes in seconds
    for video in all_videos:
        duration = video.get("duration", "00:00:00")  # format is "HH:MM:SS"
        if isinstance(duration, str):
            duration_parts = duration.split(":")
            if len(duration_parts) == 3:
                hours, minutes, seconds = map(int, duration_parts)
                total_seconds = hours * 3600 + minutes * 60 + seconds
            else:
                continue
        else:
            raise TypeError("duration must be a string")
        if total_seconds < minimal_length:
            continue
        video["secondsDuration"] = total_seconds
        relevant_videos.append(video)
    print(f"Found {len(relevant_videos)} relevant videos.")
    print(f"Total duration of relevant videos: {sum(video['secondsDuration'] for video in relevant_videos)} seconds")
    with open(os.path.join(DATA_DIR, "long_videos.json"), 'w+', encoding='utf-8') as f:
        json.dump(relevant_videos, f, ensure_ascii=False, indent=4)




def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    all_videos = []
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            all_videos = json.load(f)
    for videos in fetch_videos():
        all_videos.extend(videos)
        with open(FILE_PATH, 'w+', encoding='utf-8') as f:
            json.dump(all_videos, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    # main()
    analyze_videos()