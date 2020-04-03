""" Interface between the Discord Bot and the script functions """
import datetime

import dataobject
import novelscraper

def convert_datetime_to_string(date: datetime.datetime):
    month = date.month if date.month >= 10 else ("0" + str(date.month))
    day = date.day if date.day >= 10 else ("0" + str(date.day))
    return "{}/{}".format(day, month)

def convert_string_to_datetime(date_str: str):
    numbers = date_str.split("/")
    time = datetime.datetime.now()
    time = time.replace(month=int(numbers[1]), day=int(numbers[0]))
    return time

def convert_dataobject_to_submission(dataobject: dataobject.DataObject):
    if dataobject.source_update_date == datetime.datetime.today().day: #Today
        return "= {} {} {} {}".format(dataobject.cases, dataobject.deaths, dataobject.recovered, dataobject.source_website)
    else: #Not today
        date = convert_datetime_to_string(dataobject.source_update_date)
        return "= {} {} {} {} {}".format(dataobject.cases, dataobject.deaths, dataobject.recovered, date, dataobject.source_website)


def create_submissions(datadict: dict):
    submissions = ""
    for country, data in datadict.items():
        submissions += country + ":\n" 
        submissions += convert_dataobject_to_submission(data) + "\n"
    return submissions

def process_check(country, checkstring):
    # Process check string and save it
    
    cases = 0
    deaths = 0
    recovered = 0
    data = {"cases": cases, "deaths": deaths, "recovered": recovered}
    novelscraper.save_dict_to_file(data, "data/currentfigures_"+country)
