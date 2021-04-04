import json
import requests
from datetime import datetime

subreddit = "FloridaMan"
beforeTimestamp = int(datetime.timestamp(datetime.now()))
# url = f"https://api.pushshift.io/reddit/search/submission/?subreddit={subreddit}&sort=desc&sort_type=created_utc&after={afterTimestamp}&before={beforeTimestamp}&size=1000"
done = False


def getTitles(beforeTimestamp):
  url = f"https://api.pushshift.io/reddit/search/submission/?subreddit={subreddit}&sort=desc&sort_type=created_utc&before={beforeTimestamp}&size=1000"
  req = requests.get(url)
  json = req.json()
  data = json['data']
  titles = [post['title'] for post in data if any(st in post['title'].lower() for st in ["florida man", "florida woman"])]
  articles_num = len(data)
  usable_num = len(titles)
  next_timestamp = data[-1]['created_utc'] if articles_num > 1 else ""
  is_over = True if articles_num < 1 else False
  print(f"fired call for {beforeTimestamp} and got {articles_num} records, {usable_num} usable")
  return (titles, next_timestamp, is_over)
title_collection = []
while done is False:
  (new_titles, next_timestamp, is_over) = getTitles(beforeTimestamp)
  if not is_over:
    beforeTimestamp = next_timestamp
  done = is_over
  title_collection = title_collection + new_titles

output = {'data': title_collection}
with open('data.json', 'w') as outfile:
  json.dump(output, outfile, indent=4)
print("Done")
