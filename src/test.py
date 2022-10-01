from YTParser import YTParser
from YTCrawler import YTCrawler
import os

def test_YTParser():
    parser = YTParser()
    print(parser.search_history)
    print(parser.subscriptions)
    print(parser.watch_history)

def test_YTCrawler():
    crawler = YTCrawler()

if __name__ == "__main__":
    # test_YTParser()
    # test_YTCrawler()
    parser = YTParser()
    crawler = YTCrawler()
    channel_ids = [sub['channel_id'] for sub in parser.subscriptions]
    print(channel_ids)
    print(crawler.subscriber_count(channel_ids))