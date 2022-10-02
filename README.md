# YouTube Data Analysis
## awareness brings healthier habits!

Easily see key and fun facts about your data just in seconds! Follow the steps:

1. Go to [Google Takeout](https://takeout.google.com/settings/takeout) and only select "Youtube and Youtube Music" (at the end). You can use "Deselect All" button at the top of the list to make this easier.
2. Once you choose "Youtube and Youtube Music," click on "Multiple Formats" button under it, and change the format for `History` from `HTML` to `JSON` and close that setting. Now, click on "All Youtube data included" button and only choose the following values: `history`, `subscriptions`.
3. Obtain a [Google Developer API Key for Youtube data](https://developers.google.com/youtube/v3/getting-started).
4. Clone this repository, and put the files (you will need to take them out of their own folders) you got under `data` folder. Either create a file named `.env` in the root directory of this repo and add `API_KEY=XXX` (where `XXX` is your API key you got from the previous step) or manually set `API_KEY` variable in the file `yt/YTCrawler.py`.
5. Run `server.py` file to start a local web server for your statistics. It might take a little while to start if your data is large. Note that to not do a lot of API requests, the data is cached and put into file named `cache.pickle` in the project root. **If you change your data contents, you need to remove cache.pickle file to update the statistics.**
6. Enjoy and reflect!