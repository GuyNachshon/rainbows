import requests

url = "https://mako-vod.akamaized.net/i/SHORT/CH22_NEWS/2025/07/ulpash_vtr2_n20250718_v1/850/index_850.m3u8"

try:
    response = requests.head(url, timeout=5)
    if response.status_code == 200:
        print("Successfully accessed URL")
    else:
        print(f"Failed to access URL. Status code: {response.status_code}")
except requests.RequestException as e:
    print(f"An error occurred: {e}")
