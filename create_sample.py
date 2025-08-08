import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, 'data')
LONG_VIDEOS_PATH = os.path.join(DATA_DIR, 'long_videos.json')
SAMPLE_PATH = os.path.join(DATA_DIR, 'sample_videos.json')

def create_sample_file():
    with open(LONG_VIDEOS_PATH, 'r', encoding='utf-8') as f:
        videos = json.load(f)
    
    sample_videos = videos[:5]
    
    with open(SAMPLE_PATH, 'w', encoding='utf-8') as f:
        json.dump(sample_videos, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    create_sample_file()
