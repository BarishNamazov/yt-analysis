import requests
import os
from dotenv import dotenv_values
import json

config = dotenv_values(os.path.join(os.path.dirname(__file__), "..", ".env"))
YT_API = "https://youtube.googleapis.com/youtube/v3"
API_KEY = config["API_KEY"] # .env file should have an api key
CHUNK = 50

class YTCrawler:
    """
    A client to do YT API requests.
    """

    def __init__(self):
        pass
        
    def get(self, resource, queries):
        queries["key"] = API_KEY
        url = f'{YT_API}/{resource}?' + "&".join(f'{key}={value}' for key, value in queries.items())
        return json.loads(requests.get(url).content)

    def subscriber_count(self, channel_ids):
        cur_idx = 0
        all_subscriber_counts = {}
        while cur_idx < len(channel_ids):
            all_subscriber_counts |= self.subscriber_count_helper(channel_ids[cur_idx : cur_idx + CHUNK])
            cur_idx += CHUNK
        return all_subscriber_counts

    def subscriber_count_helper(self, channel_ids):
        id = ",".join(channel_ids)
        part = "statistics"
        stats = self.get("channels", {
            'id': id,
            'part': part
        })
        return {item["id"]: item["statistics"]["subscriberCount"] for item in stats["items"]}