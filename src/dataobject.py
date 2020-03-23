import novelscraper

class DataObject:
    """Contains the data scraped from a country"""
    def __init__(self, scraper):
        self.deaths = 0
        self.cases = 0
        self.recovered = 0
        self.tested = 0
        self.hospitalised = 0
        self.intensive_care = 0
        self.country_name = scraper.country_name
        self.iso_code = scraper.iso_code
        self.source_website = scraper.source_website

    def __str__(self):
        """ Function to give nice printing results for print() """
        return "{}: {} cases, {} deaths, {} recovered, {} tested, {} hospitalized".format(self.country_name, self.cases, self.deaths, self.recovered, self.tested, self.hospitalised)