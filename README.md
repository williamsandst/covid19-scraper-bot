## A Covid19 data scraping bot  
This is a discord bot made using Discord Py, designed to scrape data surrounding the 2020 Covid19 pandemic for the website www.covid19-intel.com. The backend is written in Python and uses Selenium to scrape websites, as well as using various available APIs for Covid19 data, such as John Hopkins and covidtracking.com. It interfaces with the data submission discord bot designed for covid19-intel.com to submit data.  

## Scope
The project currently tracks all European countries as well as all US states, through their various government primary sources for Covid19 statistics.

## Data scraping  
The bot uses Selenium, a tool for automating full loading of websites. This is needed, as many websites have Javascript which needs to be run before data can be found. Once the website is loaded in, BeautifulSoup with lxml is used to parse the html and extract the plain text. This plain text is then run through a simplified learning model to extract the appropriate numbers. The learning model is created for a website through a training approach, where the appropriate numbers are given and the model learns where to find them in the text. For most websites this approach works very well and keeps working past minor design changes of the website. A few special cases require a more manual approach, where BeautifulSoup is used to do more standard scraping based on HTML elements.  

## Dependencies (Python 3):  
**Selenium** - for scraping websites          `pip3 install selenium`  
Selenium uses Firefox (Gecko) webdriver, which can be downloaded here: https://github.com/mozilla/geckodriver/releases  
**BeautifulSoup** - for parsing scraped html  `pip3 install beautifulsoup`   
**Lxml**     - for parsing scraped html       `pip3 install lxml`  
**Html5Lib** - for parsing scraped html       `pip3 install html5lib`  
**Discord py** - Discord python API           `pip3 install discord`  
**Dateutil** - helper for parsing dates       `pip3 install python-dateutil`  
**Stringdist** - lib for Dam-Lev string dist  `pip3 install StringDist`  
**Dotenv** - for loading .env preferences     `pip3 install python-dotenv`  
**PyDrive** - for downloading from Drive      `pip3 install PyDrive`  
**xlrd** - for parsing excel files            `pip3 install xlrd`  
**Pndas** - for parsing excel files           `pip3 install pandas`  
