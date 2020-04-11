""" Interface between the Discord Bot and the script functions """
import datetime
import dataobject
import novelscraper

import pandas as pd

def convert_datetime_to_string(date: datetime.datetime):
    month = date.month if date.month >= 10 else ("0" + str(date.month))
    day = date.day if date.day >= 10 else ("0" + str(date.day))
    return "{}/{}".format(day, month)

def convert_string_to_datetime(date_str: str):
    numbers = date_str.split("/")
    time = datetime.datetime.now()
    time = time.replace(month=int(numbers[1]), day=int(numbers[0]))
    return time

def get_date_range(datebegin, dateend) -> list:
    return pd.date_range(start=datebegin, end=dateend).to_pydatetime().tolist()

def convert_dataobject_to_submission(dataobject: dataobject.DataObject):
    if dataobject.source_update_date.month == datetime.datetime.today().month and dataobject.source_update_date.day == datetime.datetime.today().day: #Today
        return "= {} {} {} {}".format(dataobject.cases, dataobject.deaths, dataobject.recovered, dataobject.source_website)
    else: #Not today
        date = convert_datetime_to_string(dataobject.source_update_date)
        return "= {} {} {} {} {}".format(dataobject.cases, dataobject.deaths, dataobject.recovered, date, dataobject.source_website)

def convert_dataobject_to_additional_data_string(dataobject: dataobject.DataObject):
    result = "Additional scrape data - "
    result += "Tested: " + str(dataobject.tested) + " " if dataobject.tested != 0 else ""
    result += "Hospitalised: " + str(dataobject.hospitalised) + " " if dataobject.hospitalised != 0 else ""
    result += "Intensive Care: " + str(dataobject.intensive_care) + " " if dataobject.intensive_care != 0 else ""
    result = result if result != "Additional scrape data - " else None
    return result


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
