import os
import pickle
from YTParser import YTParser
from YTCrawler import YTCrawler
import math
from collections import Counter

DATA_DEFAULT_PATH = os.path.join(os.path.dirname(__file__), "..", "data")
DATA_CACHE_DEFAULT_PATH = os.path.join(
    os.path.dirname(__file__), "..", "cache.pickle")

YT_CATEGORIES = {
    "1": "Film & Animation",
    "2": "Autos & Vehicles",
    "10": "Music",
    "15": "Pets & Animals",
    "17": "Sports",
    "18": "Short Movies",
    "19": "Travel & Events",
    "20": "Gaming",
    "21": "Videoblogging",
    "22": "People & Blogs",
    "23": "Comedy",
    "24": "Entertainment",
    "25": "News & Politics",
    "26": "Howto & Style",
    "27": "Education",
    "28": "Science & Technology",
    "29": "Nonprofits & Activism",
    "30": "Movies",
    "31": "Anime/Animation",
    "32": "Action/Adventure",
    "33": "Classics",
    "34": "Comedy",
    "35": "Documentary",
    "36": "Drama",
    "37": "Family",
    "38": "Foreign",
    "39": "Horror",
    "40": "Sci-Fi/Fantasy",
    "41": "Thriller",
    "42": "Shorts",
    "43": "Shows",
    "44": "Trailers",
}

# def estimate_video_watch_duration(video_duration):

class Aggregator:
    def __init__(self, data_path=DATA_DEFAULT_PATH, data_cache_path=DATA_CACHE_DEFAULT_PATH):
        self.parsed = YTParser(data_path)
        self.crawler = YTCrawler()

        try:
            with open(data_cache_path, 'rb') as f:
                cached = pickle.load(f)
                self.sub_count = cached['sub_count']
                self.video_details = cached['video_details']
                self.video_watch_time = cached['video_watch_time']
        except:
            # channel_id -> sub count
            self.sub_count = self.crawler.subscriber_count(
                [sub['channel_id'] for sub in self.parsed.subscriptions])

            # video id -> video metadata
            self.video_details = self.crawler.video_details(
                [item["video_id"] for item in self.parsed.watch_history if not item["is_ad"]])

            # video id -> time when user watched it
            self.video_watch_time = {item["video_id"]: item["time"]
                                     for item in self.parsed.watch_history}

            with open(data_cache_path, 'wb') as f:
                pickle.dump({
                    'sub_count': self.sub_count,
                    'video_details': self.video_details,
                    'video_watch_time': self.video_watch_time
                }, f)

    def number_of_ads_watched(self):
        return sum(entry['is_ad'] for entry in self.parsed.watch_history)

    def total_watched_ad_duration(self):
        return self.number_of_ads_watched() * 15  # seconds

    def total_watched_video_duration(self):
        return self.total_watched_ad_duration() + self.estimate_watch_duration([item["video_id"] for item in self.parsed.watch_history if not item["is_ad"]])
   
    def estimate_video_watch_duration(self, duration):
        video_length = duration/60 
        watch_duration = (-4 * math.sqrt(video_length-1)+70) * (video_length/100)

    def estimate_watch_duration(self, video_ids):
        total_duration = 0
        for video_id in video_ids:
            total_duration += self.estimate_video_watch_duration(
                self.video_details[video_id]["duration"].total_seconds()
            )
        return total_duration
    
    def remove_single_entries(self):
        return [x for x, count in Counter(self).items() if count > 1]
    
    def most_frequent(self):
        duplicates = self.remove_single_entries(self)
        return dict((entry, duplicates.count(entry)) for entry in set(duplicates))
    
    def most_viewed_channels(self, channel_ids):
        channel_counts = dict((entry, self.channel_ids.count(entry)) for entry in set((self)))
        
