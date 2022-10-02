import requests
import os
from dotenv import dotenv_values
import json
import functools
import isodate

config = dotenv_values(os.path.join(os.path.dirname(__file__), "..", ".env"))
YT_API = "https://youtube.googleapis.com/youtube/v3"
API_KEY = config["API_KEY"] # .env file should have an api key
CHUNK_SIZE = 50

class YTCrawler:
    """
    A client to do YT API requests.
    """

    def __init__(self):
        pass

    def get(self, resource, queries):
        print("HEY I AM MAKING A GET RWQUEST!!!")
        queries["key"] = API_KEY
        url = f'{YT_API}/{resource}?' + "&".join(f'{key}={value}' for key, value in queries.items())
        return json.loads(requests.get(url).content)

    @staticmethod
    def chunkify(l):
        """
        divides l into lists of size at most 50 and returns list of those chunks
        """
        cur_idx = 0
        chunks = []
        while cur_idx < len(l):
            chunks.append(l[cur_idx : cur_idx + CHUNK_SIZE])
            cur_idx += CHUNK_SIZE
        return chunks

    def subscriber_count(self, channel_ids):
        def subscriber_count_helper(channel_ids):
            id = ",".join(channel_ids)
            part = "statistics"
            stats = self.get("channels", {
                'id': id,
                'part': part
            })
            return {item["id"]: item["statistics"]["subscriberCount"] for item in stats["items"]}
        return functools.reduce(lambda c1, c2: c1 | c2, map(subscriber_count_helper, self.chunkify(channel_ids)), {})

    def video_details(self, video_ids):
        def video_details_helper(video_ids):
            id = ",".join(video_ids)
            part = "snippet,contentDetails,statistics"
            stats = self.get("videos", {
                'id': id,
                'part': part
            })
            return {
                item["id"]: {
                    'video_title': item["snippet"]["title"],
                    'channel_id': item["snippet"]["channelId"],
                    'category_id': item["snippet"]["categoryId"],
                    'duration': isodate.parse_duration(item["contentDetails"]["duration"]),
                    'view_count': item["statistics"]["viewCount"]
                }
                for item in stats["items"]
            }
        video_ids = list(set(video_ids))
        return functools.reduce(lambda c1, c2: c1 | c2, map(video_details_helper, self.chunkify(video_ids)), {})