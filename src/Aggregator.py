import os
from YTParser import YTParser

DATA_DEFAULT_PATH = os.path.join(os.path.dirname(__file__), "..", "data")

class Aggregator:
    def __init__(self, data_path = DATA_DEFAULT_PATH):
        self.parsed = YTParser(data_path)
    
    def number_of_ads_watched(self):
        return sum(entry['is_ad'] for entry in self.parsed.watch_history)

            