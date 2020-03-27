""" Interface between the Discord Bot and the script functions """
import dataobject

def convert_dataobject_to_submission(dataobject: dataobject.DataObject):
    return "= {} {} {} {}".format(dataobject.cases, dataobject.deaths, dataobject.recovered, dataobject.source_website)

def create_submissions(datadict: dict):
    submissions = ""
    for country, data in datadict.items():
        submissions += country + ":\n" 
        submissions += convert_dataobject_to_submission(data) + "\n"
    return submissions