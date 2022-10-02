import os
import pickle
from yt.YTParser import YTParser
from yt.YTCrawler import YTCrawler
from collections import Counter
from yt import DATA_DEFAULT_PATH

DATA_CACHE_DEFAULT_PATH = os.path.join(
    os.path.dirname(__file__), "..", "cache.pickle")

YT_CATEGORIES = {
    "0": "Unknown",
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

EXCLUDE_WORDS = {
    "the", "be", "to", "of", "and", "a", "in", "that", "have", "I", "it", "for", "not", "on", "with", "he", "as",
    "you", "do", "at", "this", "but", "his", "by", "from", "they", "we", "say", "she", "or", "an", "will", "my", 
    "one", "all", "would", "there", "their", "what", "so", "up", "out", "if", "about", "who", "get", "which", "go", 
    "me", "how"
}


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
        self.channel_name = {e['channel_id']: e['channel_name'] for e in self.parsed.subscriptions}
        self.parsed.watch_history = [e for e in self.parsed.watch_history if e['video_id'] in self.video_details or e.get('is_ad', False)]
        # the line above should only keep videos watched with public data available


    def number_of_videos_watched(self):
        return len(self.parsed.watch_history)

    def number_of_ads_watched(self):
        return sum(entry['is_ad'] for entry in self.parsed.watch_history)

    def total_watched_ad_duration(self):
        return self.number_of_ads_watched() * 15  # seconds

    def total_watched_video_duration(self):
        return self.total_watched_ad_duration() + self.estimate_watch_duration([item["video_id"] for item in self.parsed.watch_history if not item["is_ad"]])

    def estimate_video_watch_duration(self, duration):
        if duration <= 60 * 8:
            return duration
        elif duration <= 60 * 30:
            return duration * 0.70
        else:
            return 60 * 30

    def estimate_watch_duration(self, video_ids):
        total_duration = 0
        for video_id in video_ids:
            total_duration += self.estimate_video_watch_duration(
                self.video_details[video_id]["duration"].total_seconds()
            )
        return total_duration

    def most_frequent_videos_watched(self, count=10):
        count = int(count)
        # video_id -> how many times watched
        video_watch_frequency = {}
        for video in self.parsed.watch_history:
            if video["is_ad"]:
                continue
            video_watch_frequency[video["video_id"]] = video_watch_frequency.get(
                video["video_id"], 0) + 1

        videos = []
        for video_id, freq in video_watch_frequency.items():
            videos.append((freq, video_id))

        videos.sort(reverse=True)
        return [(self.video_details[id[1]]["video_title"], id[0]) for id in videos[:count]]

    def most_viewed_channels(self, count=10, mode="freq"):
        """
        if mode=time, return most time spent on channel,
        if mode=freq, return most number of videos watched
        """
        count = int(count)
        # channel_name -> how many times watched/spent time on
        channel_watch_time = {}
        for video in self.parsed.watch_history:
            if video["is_ad"]:
                continue
            channel_watch_time[video["channel_name"]] = channel_watch_time.get(
                video["channel_name"], 0) + (1 if mode == "freq" else self.estimate_watch_duration([video["video_id"]]))

        videos = []
        for video_id, freq in channel_watch_time.items():
            videos.append((freq, video_id))

        videos.sort(reverse=True)
        return [(id[1], id[0]) for id in videos[:count]]

    def most_frequent_categories(self, count=10, mode="freq"):
        count = int(count)
        # category_id -> how many times watched/time spent on
        category_watch_time = {}
        for video in self.parsed.watch_history:
            if video["is_ad"]:
                continue
            video_category = self.video_details[video["video_id"]]["category_id"]
            category_watch_time[video_category] = category_watch_time.get(
                video_category, 0) + (1 if mode == "freq" else self.estimate_watch_duration([video["video_id"]]))

        videos = []
        for video_id, freq in category_watch_time.items():
            videos.append((freq, video_id))

        videos.sort(reverse=True)
        return [(YT_CATEGORIES[id[1]], id[0]) for id in videos[:count]]

    def most_searched_words(self, count=10):
        count = int(count)
        freqs = Counter(sum([entry["query"].split() for entry in self.parsed.search_history], start=[]))
        for word in EXCLUDE_WORDS:
            if word in freqs:
                del freqs[word]
        return freqs.most_common(count)
    
    def most_popular_channels(self, count=10):
        count = int(count)
        subs = []
        for sub_id, sub_count in self.sub_count.items():
            subs.append((int(sub_count), self.channel_name[sub_id]))
        subs.sort(reverse=True)
        return [(e[1], e[0]) for e in subs[:count]]