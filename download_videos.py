import os
import json
import subprocess
from multiprocessing import Pool
from tqdm import tqdm

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, 'data')
VIDEOS_WITH_M3U8_PATH = os.path.join(DATA_DIR, 'videos_with_m3u8.json')
DOWNLOAD_DIR = os.path.join(DATA_DIR, 'downloads')

def download_video(video):
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    video_id = video['videoId']
    m3u8_url = video['m3u8_url']
    output_path = os.path.join(DOWNLOAD_DIR, f"{video_id}.mp4")

    if os.path.exists(output_path):
        print(f"Video {video_id} already downloaded. Skipping.")
        return

    command = [
        'ffmpeg',
        '-i', m3u8_url,
        '-c', 'copy',
        '-bsf:a', 'aac_adtstoasc',
        output_path
    ]

    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"Successfully downloaded {video_id}")
    except subprocess.CalledProcessError as e:
        print(f"Error downloading {video_id}: {e.stderr}")

def main():
    with open(VIDEOS_WITH_M3U8_PATH, 'r', encoding='utf-8') as f:
        videos = json.load(f)

    with Pool() as pool:
        list(tqdm(pool.imap(download_video, videos), total=len(videos), desc="Downloading videos"))

if __name__ == "__main__":
    main()
