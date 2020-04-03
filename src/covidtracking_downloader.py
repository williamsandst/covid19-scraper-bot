import requests
import json
import time
import datetime

import dataobject

state_long_to_shorthand_dict = {
    "Alabama":	"AL",
    "Alaska":	"AK",
    "Arizona":	"AZ",
    "Arkansas":	"AR",
    "California":	"CA",
    "Colorado":	"CO",
    "Connecticut":	"CT",
    "Delaware":	"DE",
    "Florida":	"FL",
    "Georgia":	"GA",
    "Hawaii":	"HI",
    "Idaho":	"ID",
    "Illinois":	"IL",
    "Indiana":	"IN",
    "Iowa":	"IA",
    "Kansas":	"KS",
    "Kentucky":	"KY",
    "Louisiana":	"LA",
    "Maine":	"ME",
    "Maryland":	"MD",
    "Massachusetts":	"MA",
    "Michigan":	"MI",
    "Minnesota":	"MN",
    "Mississippi":	"MS",
    "Missouri":	"MO",
    "Montana":	"MT",
    "Nebraska":	"NE",
    "Nevada": 	"NV",
    "New Hampshire":	"NH",
    "New Jersey":	"NJ",
    "New Mexico":	"NM",
    "New York":	"NY",
    "North Carolina":	"NC",
    "North Dakota":	"ND",
    "Ohio":   	"OH",
    "Oklahoma":	"OK",
    "Oregon": 	"OR",
    "Pennsylvania":	"PA",
    "Rhode Island":	"RI",
    "South Carolina":	"SC",
    "South Dakota":	"SD",
    "Tennessee":	"TN",
    "Texas":	"TX",
    "Utah":	"UT",
    "Vermont":	"VT",
    "Virginia":	"VA",
    "Washington":	"WA",
    "West Virginia":	"WV",
    "Wisconsin":	"WI",
    "Wyoming":	"WY",
    "District of Colombia": "DC",
    "American Samoa":   "AS",
    "Guam":     "GU",
    "Northern Mariana Islands": "MP",
    "Puerto Rico": "PR",
    "US Virgin Islands": "VI"}

state_shorthand_to_long_dict = {v: k for k, v in state_long_to_shorthand_dict.items()}

def convert_state_shorthand_to_long(state):
    if state.upper() in state_shorthand_to_long_dict:
        return state_shorthand_to_long_dict[state.upper()]
    else:
        return state

def getJSONFromLink(link):
    #page = requests.get(link)
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

    data = getJSONFromLink("https://covidtracking.com/api/states/daily?date=" + now_date_str)
    if data["error"] == True:
        print("No data at this date, trying the date before")
        print("Retrieving {} data for {} from the Covidtracking.com API".format(state, yesterday_date_str))
        data = getJSONFromLink("https://covidtracking.com/api/states/daily?date=" + yesterday_date_str)
        date = date - datetime.timedelta(days=1)
    
    final_dict = {}

    for i in data:
        state2 = i["state"]
        if 'death' in i:
            death = 0 if i["death"] == None else i["death"]
        else:
            death = -1
        total = 0 if i["positive"] == None else i["positive"]
        final_dict.setdefault(state2, [])
        final_dict[state2] += [state2, date, total, death]

    if state in final_dict:
        state_data = final_dict[state]
        result.cases = state_data[2]
        result.deaths = state_data[3]
        #result.recovered = state_data[3]
        result.source_update_date = date
    else:
        print("Error: State not found in API data")
        

    return result