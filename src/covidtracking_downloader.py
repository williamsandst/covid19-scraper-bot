import requests
import json
import time
import datetime

import dataobject
import novelscraper
import dateutil.parser

CACHE_TIME_LIMIT_SECONDS = 20

def check_for_file_cache():
    try:
        data = novelscraper.load_dict_from_file("data/covidtracking_cache.cache")
        seconds = data["time"]
        now = datetime.datetime.now()
        now_seconds = int(now.hour * 3600 + now.minute * 60 + now.second)
        if now_seconds < (seconds + CACHE_TIME_LIMIT_SECONDS):
            return data
        else: #Cache is too old, redownload
            print("Cache is old, revalidating")
            return None
    except: #Something went wrong loading the cache, redownload
        print("Covidtracking Cache Error")
        return None

def save_cache(data):
    date = datetime.datetime.now()
    data["time"] = int(date.hour * 3600 + date.minute * 60 + date.second)
    novelscraper.save_dict_to_file(data, "data/covidtracking_cache.cache", )

def getJSONFromLink(link):
    s = requests.Session()
    page = s.get(link)
    cookies = dict(page.cookies)
    data = json.loads(page.content)
    return data

def convert_datetime_to_datestring(date: datetime.datetime):
    month = date.month if date.month >= 10 else ("0" + str(date.month))
    day = date.day if date.day >= 10 else ("0" + str(date.day))
    return "{}{}{}".format(date.year, month, day)


def scrape(state: str, result, date = datetime.datetime.now()):
    now_date_str = convert_datetime_to_datestring(date)
    yesterday_date_str = convert_datetime_to_datestring(date - datetime.timedelta(days=1))

    print("Retrieving {} data for {} from the Covidtracking.com API".format(state, now_date_str))

    final_dict = {}
    data = check_for_file_cache()
    cache = True

    if data == None:
        cache = False
    else:
        final_dict = data

    if cache == False:
        data = getJSONFromLink("https://covidtracking.com/api/states/daily?date=" + now_date_str)
        date_str = now_date_str
        if data["error"] == True:
            print("No data at this date, trying the date before")
            print("Retrieving {} data for {} from the Covidtracking.com API".format(state, yesterday_date_str))
            data = getJSONFromLink("https://covidtracking.com/api/states/daily?date=" + yesterday_date_str)
            date = date - datetime.timedelta(days=1)
            date_str = yesterday_date_str
    

        for i in data:
            state2 = i["state"]
            if 'death' in i:
                death = 0 if i["death"] == None else i["death"]
            else:
                death = -1
            total = 0 if i["positive"] == None else i["positive"]
            final_dict.setdefault(state2, [])
            final_dict[state2] += [state2, date_str, total, death]

    if state in final_dict:
        state_data = final_dict[state]
        result.cases = state_data[2]
        result.deaths = state_data[3]
        #result.recovered = state_data[3]
        result.source_update_date = date
    else:
        print("Error: State not found in API data")

    if not cache:
        save_cache(final_dict)
        

    return result