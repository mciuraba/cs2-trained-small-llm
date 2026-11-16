import requests
import json

BASE_URL = 'https://cs2tracker.gg/api/player/chat-log'

def fetch_chat_logs(steam_id: str, matches: int=50) -> dict:
    params = {
        "steamid": steam_id,
        "scope": "all",
        "matches": matches
    }

    response = requests.get(BASE_URL, params=params, timeout=25)

    print("Status:", response.status_code)
    print("URL:", response.url)
    print("Headers:", response.headers)
    print("Response:", response.text[:1000])

    response.raise_for_status()

steam_id = "76561198171178965"
data = fetch_chat_logs(steam_id)

print(data["matches"][0])