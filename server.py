import os
import json
import mimetypes

from wsgiref.simple_server import make_server
from yt.Aggregator import Aggregator

print("initializing Youtube data...")
yt = Aggregator()
print("done initializing Youtube data!")
print()

cur_dir = os.path.realpath(os.path.dirname(__file__))
app_root = os.path.join(cur_dir, 'ui')

def parse_get(environ):
    queries = environ['QUERY_STRING'].split("&")
    result = {}
    for query in queries:
        if not query:
            continue
        q = query.split("=")
        print(q)
        result[q[0]] = q[1]
    return result

special_routes = {
    '/number_of_videos_watched': lambda params: yt.number_of_videos_watched(),
    '/total_watch_time': lambda params: yt.total_watched_video_duration(),
    '/number_of_ads_watched': lambda params: yt.number_of_ads_watched(),
    '/total_ads_watch_time': lambda params: yt.total_watched_ad_duration(),
    '/most_watched_category': lambda params: yt.most_frequent_categories(1)[0],
    '/most_searched_word': lambda params: yt.most_searched_words(1)[0],

    '/most_searched_words': lambda params: yt.most_searched_words(params.get("count", 10)),
    '/most_frequent_videos': lambda params: yt.most_frequent_videos_watched(params.get("count", 10)),
    '/most_frequent_categories': lambda params: yt.most_frequent_categories(count=params.get("count", 10), mode=params.get("mode", "freq")),
    '/most_frequent_channels': lambda params: yt.most_viewed_channels(count=params.get("count", 10), mode=params.get("mode", "freq")),
    '/most_popular_channels': lambda params: yt.most_popular_channels(count=params.get("count", 10)),
}

def application(environ, start_response):
    path = environ.get('PATH_INFO', '/') or '/'
    params = parse_get(environ)

    print(f'requested {path}, params: {params}')

    if path in special_routes:
        type_ = 'application/json'
        status = '200 OK'
        body = json.dumps(special_routes[path](params)).encode('utf-8')
    else:
        if path == '/':
            # main page
            static_file = 'index.html'
        else:
            if path.startswith('/ui/'):
                static_file = path[4:]
            else:
                static_file = path[1:]

        test_fname = os.path.join(app_root, static_file)
        if os.path.isfile(test_fname):
            with open(test_fname, 'rb') as f:
                body = f.read()
            status = '200 OK'
            type_ = mimetypes.guess_type(test_fname)[0] or 'text/plain'
        else:
            body = b'File not found: %r' % test_fname
            status = '404 FILE NOT FOUND'
            type_ = 'text/plain'
    len_ = str(len(body))
    headers = [('Content-type', type_), ('Content-length', len_)]
    start_response(status, headers)
    return [body]


if __name__ == '__main__':
    PORT = 8080
    print(f'starting server.  navigate to http://localhost:{PORT}/')
    with make_server('', PORT, application) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("Shutting down.")
            httpd.server_close()