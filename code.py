import requests
import typing
from urllib.parse import urljoin

YT_API_KEY = "AIzaSyC5qR2mBjEdyxnjEs4XNosWfTes8oS6ik8"
YT_API = "https://www.googleapis.com/youtube/v3/"

def yt_get(resource: str, query: dict[str, str]):
    query["key"] = YT_API_KEY
    url_with_queries = f"{urljoin(YT_API, resource)}?" + "&".join(f"{key}={val}" for key, val in query.items())
    return requests.get(url_with_queries)

my_subs = yt_get("subscriptions", {'part': 'snippet', 'channelId': 'UCLFfnx-IqaFXKFC9AJAYCGA'})

print(my_subs)
print(my_subs.content)