import novelscraper
import datetime

class DataObject:
    """Contains the data scraped from a country"""
    def __init__(self, scraper):
        self.deaths = 0
        self.cases = 0
        self.recovered = 0
        self.tested = 0
        self.hospitalised = 0
        self.intensive_care = 0
        self.suspected_cases = 0
        self.source_update_date = None
        self.scrape_date = datetime.datetime.now()
        self.country_name = scraper.country_name
        self.iso_code = scraper.iso_code
        self.screenshot_path = None
        if scraper.report_website == None:
            self.source_website = scraper.source_website
        else:
            self.source_website = scraper.report_website

    def __str__(self):
        """ Function to give nice printing results for print() """
        output = "{}: {} cases, {} deaths, {} recovered, {} tested, {} hospitalized, {} in ICU".format(self.country_name, self.cases, self.deaths, self.recovered, self.tested, self.hospitalised, self.intensive_care)
        #output += "\n{}: Source: [{}], updated at {}, retrieved at {}".format(self.country_name, self.source_website[12:35] + (self.source_website[35:] and '..'), 
        #self.source_update_date, self.scrape_date)
        output += "\nSource: {}".format(self.source_website)
        return output

    def update_by_str(self, string: str, value) -> None:
        setattr(self, string, value)

    def update_by_str_dict(self, str_dict):
        for key, value in str_dict.items():
            self.update_by_str(key, value)
