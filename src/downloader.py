import requests
import json
import time
import datetime
import csv
import codecs
import logging
from contextlib import closing

import dateutil.parser
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
import pandas as pd

import dataobject
import novelscraper
import bot_data
import config

log = logging.getLogger("DWNL")

def check_for_file_cache(date):
    try:
        data = novelscraper.load_dict_from_file("data/covidtracking_cache_{}_{}_{}.cache".format(date.day, date.month, date.hour))
        seconds = data["time"]
        now = datetime.datetime.now()
        now_seconds = int(now.hour * 3600 + now.minute * 60 + now.second)
        if now_seconds < (seconds + config.CACHE_TIME_LIMIT_SECONDS):
            log.info("Covidtracking.com Cache is valid at age {} sec".format(now_seconds-seconds))
            return data
        else: #Cache is too old, redownload
            log.info("Covidtracking Cache is old, revalidating")
            return None
    except: #Something went wrong loading the cache, redownload
        log.warning("Covidtracking Cache Error")
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

def scrape_covidtracking(state: str, result, date = datetime.datetime.now(), check_yesterday_if_error=False):
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
        log.info("Retrieving {} data for {} from the Covidtracking.com API".format(state, now_date_str))
        data = getJSONFromLink("https://covidtracking.com/api/states/daily?date=" + now_date_str)
        if not isinstance(data, list) and data["error"] == True:
            log.warning("Covidtracking.com has no data for date {}".format(now_date_str))
            result.data_validity = "Error retrieving covidtracking.com data from date {}, has the source updated for this day yet?".format(now_date_str)
            now_cache = {}
        else:
            result.data_validity = "OK"
            date_str = now_date_str
            now_cache = add_state_data_to_dict(data, date_str)
        save_now_cache = True
 
    if yesterday_cache == None:
        final_dict = {}
        log.info("Retrieving {} data for {} from the Covidtracking.com API".format(state, yesterday_date_str))
        data = getJSONFromLink("https://covidtracking.com/api/states/daily?date=" + yesterday_date_str)
        if not isinstance(data, list) and data["error"] == True:
            log.warning("Covidtracking.com has no data for date {}".format(yesterday_date_str))
            result.data_validity = "Error retrieving covidtracking.com data for this date {}, has the source updated for this day yet?".format(yesterday_date_str)
            yesterday_cache = {}
        else:
            result.data_validity = "OK"
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

def scrape_hopkins(scrape_country, scrape_province, scrape_country_iso_code, result, date, ):
    result.source_update_date = date
    
    scrape_country = scrape_country.translate({ord('-'): " "})
    scrape_province = scrape_province.translate({ord('-'): " "})

    ignore_provinces = (scrape_province == scrape_country)
 
    cases_csv_path = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
    deaths_csv_path = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
    recovered_csv_path = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"
    
    cases_fields, cases_rows = get_csv_from_link(cases_csv_path)
    deaths_fields, deaths_rows = get_csv_from_link(deaths_csv_path)
    recovered_fields, recovered_rows = get_csv_from_link(recovered_csv_path)

    day_index = get_date_index(date, cases_fields)

    if day_index == -1:
        result.data_validity = "Error retrieving John Hopkins data for this date {}, has the source updated for this day yet?".format(date.__str__())
        return result

    country_found = False
    for row in cases_rows:
        country = row[1]
        province = row[0]
        if country.lower() == scrape_country.lower() and (ignore_provinces or scrape_province.lower() == province.lower()):
            country_found = True
            result.cases += int(row[day_index])

    for row in deaths_rows:
        country = row[1]
        province = row[0]
        if country.lower() == scrape_country.lower() and (ignore_provinces or scrape_province.lower() == province.lower()):
            result.deaths += int(row[day_index])

    for row in recovered_rows:
        country = row[1]
        province = row[0]
        if country.lower() == scrape_country.lower() and (ignore_provinces or scrape_province.lower() == province.lower()):
            result.recovered += int(row[day_index])

    if country_found == False:
        result.data_validity = "John Hopkins has data for this date, but the country {} cannot be located. There might be a naming conflict.".format(scrape_country)

    return result


def download_sheet_from_drive():
    # Create GoogleDrive instance with authenticated GoogleAuth instance.
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()

    drive = GoogleDrive(gauth)

    #list_of_all_files = drive.ListFile({'q': 'sharedWithMe'})
    #for country in list_of_all_files:
        #print("test")

    europe_id = "1RIXWF7wCX-CihFQzNPfb4t26_t9NlReHj2GH2q3Euac"
    usa_id = "1YNVvKZp3Vywcb6Klggpu3WdBfT3nSzSYF8zCK-iUvVE"
    canada_id = "1TQdiv_WKkIhu4UQk1ORG5hYVfqwV9Rl2vWaUnlosrJs"

    mime_type_sheets = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    # Europe
    log.info("Downloading Europe sheet from Google Drive...")
    file1 = drive.CreateFile({"id": europe_id})
    file1.GetContentFile("data/drive/europe.xlsx", mimetype=mime_type_sheets)
    log.info("Download complete")

    # US
    log.info("Downloading United States sheet from Google Drive...")
    file1 = drive.CreateFile({"id": usa_id})
    file1.GetContentFile("data/drive/us.xlsx", mimetype=mime_type_sheets)
    log.info("Download complete")

    # Canada
    log.info("Downloading Canada sheet from Google Drive...")
    file1 = drive.CreateFile({"id": canada_id})
    file1.GetContentFile("data/drive/canada.xlsx", mimetype=mime_type_sheets)
    log.info("Download complete")

def check_drive_cache():
    cache = False
    date = datetime.datetime.now()
    try:
        cache_data = novelscraper.load_dict_from_file("data/drive/sheet_cache_{}_{}_{}.cache".format(date.day, date.month, date.hour))
        seconds = cache_data["time"]
        now = datetime.datetime.now()
        now_seconds = int(now.hour * 3600 + now.minute * 60 + now.second)
        if now_seconds < (seconds + config.DRIVE_CACHE_TIME_LIMIT_SECONDS):
            log.info("Drive Cache is valid at age {} sec".format(now_seconds-seconds))
            cache = True
        else: #Cache is too old, redownload
            log.info("Drive Cache is old, revalidating")
            cache = False
    except:
        cache = False
        log.warning("Drive Cache error")

    if not cache: #Download sheet
        download_sheet_from_drive()
        cache_data = {}
        date = datetime.datetime.now()
        cache_data["time"] = int(date.hour * 3600 + date.minute * 60 + date.second)
        novelscraper.save_dict_to_file(cache_data, "data/drive/sheet_cache_{}_{}_{}.cache".format(date.day, date.month, date.hour))

def channel_to_sheet_country(channel):
    # Remove '-' and make every word first character capitalised
    words = channel.split("-")
    country = ""
    for word in words:
        if word != "and":
            country += word[0].upper() + word[1:] + " "
        else:
            country += word + " "

    return country.strip()

def get_sheet_date_index(date: datetime.datetime, days):
    for i, day in enumerate(days):
        if date.month == day.month and date.day == day.day:
            return i
    return -1

def check_from_sheet(country, country_iso_code, date):
    log.info("Retrieving data from the Google Sheet database...")
    result = dataobject.DataObject()
    result.date = date
    result.country_name = country
    result.source_update_date = date

    check_drive_cache()

    sheet_country = channel_to_sheet_country(country)

    sheet_path = ""
    if country in bot_data.europe_channels:
        sheet_path = 'data/drive/europe.xlsx'
    elif country in bot_data.us_channels:
        sheet_path = 'data/drive/us.xlsx'
    elif country in bot_data.canada_channels:
        sheet_path = 'data/drive/canada.xlsx'

    if sheet_path != "":
        sheet = pd.read_excel(sheet_path, sheet_name=sheet_country)

        dates = sheet[sheet.columns[0]].tolist()
        cases = sheet[sheet.columns[1]].tolist()
        deaths = sheet[sheet.columns[2]].tolist()
        recovered = sheet[sheet.columns[3]].tolist()

        index = get_sheet_date_index(date, dates)
        if index == -1:
            result.data_validity = "Could not find specified date in the Google Sheet data. Has a new date been added to the sheet yet?"
            return result

        result.cases = int(cases[index])
        result.deaths = int(deaths[index])
        result.recovered = int(recovered[index])

    return result

#check_from_sheet("Sweden", "SE", datetime.datetime.now())
