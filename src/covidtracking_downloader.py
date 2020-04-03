import requests
import json
import time
import datetime

import dataobject
import novelscraper
import dateutil.parser

CACHE_TIME_LIMIT_SECONDS = 20

def check_for_file_cache(date):
    try:
        data = novelscraper.load_dict_from_file("data/covidtracking_cache_{}_{}_{}.cache".format(date.day, date.month, date.hour))
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

def save_cache(data, savedate):
    date = datetime.datetime.now()
    data["time"] = int(date.hour * 3600 + date.minute * 60 + date.second)
    novelscraper.save_dict_to_file(data, "data/covidtracking_cache_{}_{}_{}.cache".format(savedate.day, savedate.month, savedate.hour))

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

def add_state_data_to_dict(data, date_str):
    final_dict = {}
    for i in data:
        state2 = i["state"]
        if 'death' in i:
            death = 0 if i["death"] == None else i["death"]
        else:
            death = 0
        if 'recovered' in i:
            recovered = 0 if i["recovered"] == None else i["recovered"]
        else:
            recovered = 0
        total = 0 if i["positive"] == None else i["positive"]
        final_dict.setdefault(state2, [])
        final_dict[state2] += [state2, date_str, total, death, recovered]
    return final_dict

def scrape(state: str, result, date = datetime.datetime.now(), check_yesterday_if_error=False):
    now_date = date
    now_date_str = convert_datetime_to_datestring(date)
    yesterday_date = date - datetime.timedelta(days=1)
    yesterday_date_str = convert_datetime_to_datestring(yesterday_date)

    result.cases = -1
    result.deaths = -1
    result.recovered = -1
    result.source_update_date = date

    now_cache = check_for_file_cache(now_date)
    save_now_cache = False
    
    if check_yesterday_if_error:
        yesterday_cache = check_for_file_cache(yesterday_date)
    else:
        yesterday_cache = {}

    save_yesterday_cache = False

    if now_cache == None:
        final_dict = {}
        print("Retrieving {} data for {} from the Covidtracking.com API".format(state, now_date_str))
        data = getJSONFromLink("https://covidtracking.com/api/states/daily?date=" + now_date_str)
        if not isinstance(data, list) and data["error"] == True:
            print("No data at this date")
            now_cache = {}
        else:
            date_str = now_date_str
            now_cache = add_state_data_to_dict(data, date_str)
        save_now_cache = True
 
    if yesterday_cache == None:
        final_dict = {}
        print("Retrieving {} data for {} from the Covidtracking.com API".format(state, yesterday_date_str))
        data = getJSONFromLink("https://covidtracking.com/api/states/daily?date=" + yesterday_date_str)
        if not isinstance(data, list) and data["error"] == True:
            print("No data at this date")
            yesterday_cache = {}
        else:
            date_str = yesterday_date_str
            yesterday_cache = add_state_data_to_dict(data, date_str)
        save_yesterday_cache = True

    for final_dict, date2 in [(now_cache, now_date), (yesterday_cache, yesterday_date)]:
        if state in final_dict:
            state_data = final_dict[state]
            result.cases = state_data[2]
            result.deaths = state_data[3]
            result.recovered = state_data[4]
            result.source_update_date = date2

    if save_now_cache:
        save_cache(now_cache, now_date)
    if save_yesterday_cache:
        save_cache(yesterday_cache, yesterday_date)
        

    return result