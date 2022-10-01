import os
import csv, json
import dateutil.parser

DATA_DEFAULT_PATH = os.path.join(os.path.dirname(__file__), "..", "data")

class YTParser:
    """
    Parser for Youtube Takeout data.
    """

    def __init__(self, data_path = DATA_DEFAULT_PATH):
        """
        data_path: the path to the folder that has youtube takeout generated files.
        """
        search_history_path = os.path.join(data_path, "search_history.json")
        watch_history_path = os.path.join(data_path, "watch_history.json")
        subscriptions_path = os.path.join(data_path, "subscriptions.csv")

        self.search_history = YTParser.parse_file(search_history_path, lambda f: json.load(f), 
                                                  transformer = YTParser.transform_search_history)

        self.watch_history = YTParser.parse_file(watch_history_path, lambda f: json.load(f),
                                                 transformer = YTParser.transform_watch_history)
        self.subscriptions = YTParser.parse_file(subscriptions_path, lambda f: [list(row) for row in csv.reader(f)][1:], # ignore header
                                                 transformer = YTParser.transform_subscriptions)
        
    @staticmethod
    def parse_file(filepath, parser, transformer = lambda data: data):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return transformer(parser(f))
        except Exception as e:
            return None

    @staticmethod
    def transform_search_history(data):
        cleaned_data = []
        for entry in data:
            detail_name = entry.get("details", [{"name": "random"}])[0]["name"]
            if detail_name == "From Google Ads":
                continue # ignore search ads, unexplainable
            cleaned_data.append({
                'query': entry['title'][13:], # "Searched for X"
                'time': dateutil.parser.isoparse(entry['time'])
            })
        return sorted(cleaned_data, key=lambda entry: entry['time'])

    @staticmethod
    def transform_watch_history(data):
        cleaned_data = []
        for entry in data:
            cleaned_entry = {}

            detail_name = entry.get("details", [{"name": "random"}])[0]["name"]
            cleaned_entry["is_ad"] = detail_name == "From Google Ads"

            cleaned_entry |= {
                'video_name': entry['title'][8:], # "Watched X"
                'video_id': entry['titleUrl'].split("\u003d")[-1], # \u003d is symbol "="
                'time': dateutil.parser.isoparse(entry['time']),
            }

            if not cleaned_entry['is_ad']:
                cleaned_entry |= {
                    'channel_name': entry['subtitles'][0]['name']
                }
            
            cleaned_data.append(cleaned_entry)
        return sorted(cleaned_data, key=lambda entry: entry['time'])

    @staticmethod
    def transform_subscriptions(data):
        cleaned_data = []
        for entry in data:
            cleaned_data.append({
                'channel_id': entry[0],
                'channel_name': entry[2]
            })
        return cleaned_data