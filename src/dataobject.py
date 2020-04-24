import novelscraper
import datetime

class DataObject:
    """Contains the data scraped from a country"""
    def __init__(self, scraper = None, date=datetime.datetime.now()):
        self.deaths = 0
        self.cases = 0
        self.recovered = 0
        self.tested = 0
        self.hospitalised = 0
        self.intensive_care = 0
        self.suspected_cases = 0
        self.data_validity = "OK"

        self.province = None # For region scrapes
        
        self.screenshot_path = None
        self.source_website = None
        self.scrape_date = date
        self.source_update_date = self.scrape_date

        if scraper != None:
            self.use_sheet_recovered = scraper.adjust_scraped_recovery_from_sheet
            self.use_sheet_deaths = scraper.adjust_scraped_deaths_from_sheet
            self.country_name = scraper.get_index_name()
            self.pretty_country_name = scraper.get_pretty_name()
            self.iso_code = scraper.iso_code
            if scraper.report_website == None:
                self.source_website = scraper.source_website
            else:
                self.source_website = scraper.report_website
        else:
            self.use_sheet_recovered = False
            self.use_sheet_deaths = False
            self.country_name = None
            self.pretty_country_name = None
            self.iso_code = None
            self.source_website = None

    def __str__(self):
        """ Function to give nice printing results for print() """
        output = "{}: {} cases, {} deaths, {} recovered, {} tested, {} hospitalized, {} in ICU".format(self.pretty_country_name, self.cases, self.deaths, self.recovered, self.tested, self.hospitalised, self.intensive_care)
        #output += "\n{}: Source: [{}], updated at {}, retrieved at {}".format(self.country_name, self.source_website[12:35] + (self.source_website[35:] and '..'), 
        #self.source_update_date, self.scrape_date)
        output += "\nSource: {}".format(self.source_website)
        return output

    def update_by_str(self, string: str, value) -> None:
        setattr(self, string, value)

    def update_by_str_dict(self, str_dict):
        for key, value in str_dict.items():
            self.update_by_str(key, value)
