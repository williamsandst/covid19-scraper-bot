""" Interface between the Discord Bot and the script functions """
import dataobject
import novelscraper

def convert_dataobject_to_submission(dataobject: dataobject.DataObject):
    return "= {} {} {} {}".format(dataobject.cases, dataobject.deaths, dataobject.recovered, dataobject.source_website)

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
