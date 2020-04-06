import requests
import json
import time
import datetime
import csv
import dateutil.parser

import codecs
from contextlib import closing

import dataobject
import novelscraper

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

def get_csv_from_link(link):
    page = requests.get(link)
    csvreader = csv.reader(codecs.iterdecode(page.iter_lines(), 'utf-8'))

    fields = [] 
    rows = [] 
  
    fields = next(csvreader) 

    # extracting each data row one by one 
    for row in csvreader: 
        rows.append(row) 
  
    return fields, rows

def get_date_index(date: datetime.datetime, fields):
    for i, day in enumerate(fields[4:], 4):
        day_split = day.split("/")
        month_num = int(day_split[0])
        day_num = int(day_split[1])
        if date.month == month_num:
            if date.day == day_num:
                return i
    return -1

def scrape_hopkins(scrape_country, scrape_country_iso_code, result, date):
    cases_csv_path = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
    deaths_csv_path = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
    recovered_csv_path = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"
    
    cases_fields, cases_rows = get_csv_from_link(cases_csv_path)
    deaths_fields, deaths_rows = get_csv_from_link(deaths_csv_path)
    recovered_fields, recovered_rows = get_csv_from_link(recovered_csv_path)

    day_index = get_date_index(date, cases_fields)

    for row in cases_rows:
        country = row[1]
        if country.lower() == scrape_country.lower():
            result.cases += int(row[day_index])

    for row in deaths_rows:
        country = row[1]
        if country.lower() == scrape_country.lower():
            result.deaths += int(row[day_index])

    for row in recovered_rows:
        country = row[1]
        if country.lower() == scrape_country.lower():
            result.recovered += int(row[day_index])

    return result
