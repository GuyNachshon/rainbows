import requests
import os
import json
import datetime
from tqdm import tqdm

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, 'data')
PLAYLISTS_DIR = os.path.join(DATA_DIR, 'playlists')

os.makedirs(PLAYLISTS_DIR, exist_ok=True)


# format: https://mako-vod.akamaized.net/i/SHORT/CH22_NEWS/YEAR/MONTH/20mahadurafull_vtr2_nYYYYMMDD_v1/850/index_850.m3u8

def fetch_m3u8_urls(year, month):
    base_url = "https://mako-vod.akamaized.net/i/SHORT/CH22_NEWS/{year}/{month}/20mahadurafull_vtr2_n{date}_v1/850/index_850.m3u8"
    urls = []

    for day in tqdm(range(1, 32), desc=f"Fetching URLs for {year}-{month:02d}"):
        date_str = f"{year}{month:02d}{day:02d}"
        url = base_url.format(year=year, month=month, date=date_str)
        try:
            print(url)
            response = requests.head(url)
            if response.status_code == 200:
                urls.append(url)
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")

    return urls


def save_m3u8_urls(year, month, urls):
    filename = f"m3u8_urls_{year}_{month:02d}.json"
    filepath = os.path.join(PLAYLISTS_DIR, filename)

    with open(filepath, 'w+') as f:
        json.dump(urls, f, indent=4)

    print(f"Saved {len(urls)} URLs to {filepath}")


def main():
    year = 2023
    month = 9  # October

    today = datetime.datetime.now()
    pbar = tqdm(total=(today.year - year) * 12 + today.month - month + 1, desc="Collecting m3u8 URLs")
    while year <= today.year:
        if year == today.year and month > today.month:
            break
        if month == 12:
            month = 1
            year += 1
        else:
            month += 1
        urls = fetch_m3u8_urls(year, month)
        if urls:
            save_m3u8_urls(year, month, urls)
        else:
            print(f"No valid URLs found for {year}-{month:02d}")
        pbar.update(1)


if __name__ == "__main__":
    main()
