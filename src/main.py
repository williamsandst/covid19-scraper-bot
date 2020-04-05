"""
Main file
This is a program which scrapes the Coronavirus confirmed cases, deaths and recovered from various countries health ministry websites
"""

import interface
from threading import Thread
import time
import datetime
import queue

from novelscraper import *
from manual_scrapers import *
from commands import *
import bot

""" 
Countries with working automated scraping:
Norway (NO)
Sweden (SE)
Denmark (DK)
Finland (FI)
Iceland (IS)
Estonia (EE)
Lativa (LV)
Lithuania (LI)
Germany (DE)
France (FR)
Spain (ES)
Italy (IT)
Portugal (PT)
Netherlands (NL)
Belgium (BE)
Switzerland (CH)
Austria (AT)

Left:
Russia (RU)
Poland (PL)
Czech Republic (CZ)
Romania (RO)
Belarus (BY) (CoronaCloud)
Ukarine (UA) (CoronaCloud)
Greece (GR) (CoronaCloud)

Andorra
Albania
Bosnia and Herzegovina
Bulgaria
Croatia
Cyprus
Hungary
Holy-see
Kosovo
Liechtenstein
Luxembourg
Malta
Moldova
Monaco
Montenegro
North Macedonia
San Marino
Slovenia
Serbia
Slovakia
"""

country_classes = {}
commands = {}
scheduled_commands = []
results = {}
discord_bot = bot.InvestigatorBot()

DISCORD_BOT_ENABLED = True

def init_europe_scrapers():
    """ Initiate the various country classes """
    # Nordic countries:
    # Norway
    scraper = NovelScraperAuto()
    scraper.country_name = "Norway" 
    scraper.iso_code = "NO"
    scraper.javascript_required = True
    scraper.source_website = "https://www.vg.no/spesial/2020/corona/"
    scraper.optimize_min_max_index_ratio = 0.1
    #scraper.training_data = {"cases": "3752", "deaths":"19", "tested":"78036", "hospitalised": "302", "intensive_care":"76"}
    country_classes[scraper.country_name.lower()] = scraper

    # Sweden
    scraper = NovelScraperAuto()
    scraper.country_name = "Sweden"
    scraper.iso_code = "SE"
    scraper.javascript_required = True
    scraper.wait_time = 10
    scraper.optimize_min_max_index_ratio = 0.1
    scraper.source_website = "https://fohm.maps.arcgis.com/apps/opsdashboard/index.html#/68d4537bf2714e63b646c37f152f1392"
    scraper.report_website = "https://www.folkhalsomyndigheten.se/smittskydd-beredskap/utbrott/aktuella-utbrott/covid-19/aktuellt-epidemiologiskt-lage/"
    #scraper.training_data = {"cases": "3046", "deaths": "92", "intensive_care": "209"}
    country_classes[scraper.country_name.lower()] = scraper

    # Denmark
    # Cases are divided up by regions, can't be parsed with auto
    scraper = NovelScraperDK()
    country_classes[scraper.country_name.lower()] = scraper

    # Iceland
    scraper = NovelScraperAuto()
    scraper.country_name = "Iceland"
    scraper.iso_code = "IS"
    scraper.javascript_required = True
    scraper.website_height = 700
    scraper.source_website = "https://e.infogram.com/7327507d-28f5-4e3c-b587-c1680bd790e6?src=embed"
    scraper.report_website = "https://www.covid.is/tolulegar-upplysingar"
    #scraper.training_data = {"cases": "890", "recovered": "97", "hospitalised":"18", "intensive_care":"6", "tested":"13613"}
    country_classes[scraper.country_name.lower()] = scraper

    # Finland
    scraper = NovelScraperAuto()
    scraper.country_name = "Finland"
    scraper.iso_code = "FI"
    scraper.javascript_required = True
    scraper.source_website = "https://korona.kans.io/"
    #scraper.training_data = {"cases": "1056", "deaths": "7", "recovered": "10"}
    country_classes[scraper.country_name.lower()] = scraper

    # Estonia
    scraper = NovelScraperAuto()
    scraper.country_name = "Estonia" 
    scraper.iso_code = "EE"
    scraper.source_website = "https://www.koroonakaart.ee/en"
    #scraper.training_data = {"cases": "640",  "deaths": "1", "recovered":"20", "tested":"9364", "hospitalised": "48"}
    country_classes[scraper.country_name.lower()] = scraper

    # Lithuania
    scraper = NovelScraperAuto()
    scraper.country_name = "Lithuania" 
    scraper.iso_code = "LI"
    scraper.source_website = "https://sam.lrv.lt/lt/naujienos/koronavirusas"
    scraper.scroll = 7
    scraper.training_data = {"cases": "382",  "deaths": "5", "recovered":"1", "tested":"6900"}
    country_classes[scraper.country_name.lower()] = scraper

    # Latvia
    scraper = NovelScraperAuto()
    scraper.country_name = "Latvia" 
    scraper.iso_code = "LV"
    scraper.source_website = "https://arkartassituacija.gov.lv/"
    #scraper.training_data = {"cases": "280", "tested":"11702", "hospitalised": "21"}
    country_classes[scraper.country_name.lower()] = scraper

    # Central Europe
    # The United Kingdom
    scraper = NovelScraperAuto()
    scraper.country_name = "United-Kingdom"
    scraper.iso_code = "GB"
    scraper.javascript_required = True
    scraper.report_link = "https://www.gov.uk/government/publications/covid-19-track-coronavirus-cases"
    scraper.source_website = "https://www.arcgis.com/apps/opsdashboard/index.html#/f94c3c90da5b4e9f9a0b19484dd4bb14"
    #scraper.training_data = {"cases": "17089", "recovered":"135", "deaths": "1019"}
    country_classes[scraper.country_name.lower()] = scraper

    # Ireland
    scraper = NovelScraperAuto()
    scraper.country_name = "Ireland"
    scraper.iso_code = "IE"
    scraper.javascript_required = True
    scraper.source_website = "https://www.gov.ie/en/news/7e0924-latest-updates-on-covid-19-coronavirus/"
    #scraper.training_data = {"cases": "2415", "deaths": "36"}
    country_classes[scraper.country_name.lower()] = scraper

    # Germany
    scraper = NovelScraperAuto()
    scraper.country_name = "Germany"
    scraper.iso_code = "DE"
    scraper.javascript_required = True
    scraper.source_website = "https://interaktiv.morgenpost.de/corona-virus-karte-infektionen-deutschland-weltweit-teaser/"
    #scraper.training_data = {"cases": "54268", "deaths": "398", "recovered":"3781"}
    country_classes[scraper.country_name.lower()] = scraper

    # France
    """# Can't scrape images. Should probably do a custom one
    scraper = NovelScraperAuto()
    scraper.country_name = "France"
    scraper.iso_code = "FR"
    scraper.javascript_required = True
    scraper.source_website = "https://www.santepubliquefrance.fr/maladies-et-traumatismes/maladies-et-infections-respiratoires/infection-a-coronavirus/articles/infection-au-nouveau-coronavirus-sars-cov-2-covid-19-france-et-monde"
    #scraper.training_data = {"cases": "54268", "deaths": "398", "recovered":"3781"}
    country_classes[scraper.country_name.lower()] = scraper
    """

    # Spain
    scraper = NovelScraperAuto()
    scraper.country_name = "Spain"
    scraper.iso_code = "ES"
    scraper.javascript_required = True
    scraper.optimize_min_max_index_ratio = 0.1
    scraper.source_website = "https://www.rtve.es/noticias/20200328/mapa-del-coronavirus-espana/2004681.shtml"
    #scraper.training_data = {"cases": "73235", "deaths": "5982", "recovered":"12285", "intensive_care":"4575"}
    country_classes[scraper.country_name.lower()] = scraper

    # Italy
    scraper = NovelScraperAuto()
    scraper.country_name = "Italy"
    scraper.iso_code = "IT"
    scraper.javascript_required = True
    scraper.optimize_min_max_index_ratio = 0.05
    scraper.source_website = "https://datastudio.google.com/u/0/reporting/91350339-2c97-49b5-92b8-965996530f00/page/RdlHB"
    #scraper.training_data = {"cases": "92472", "deaths": "10023", "recovered":"12384", "intensive_care":"3856", "hospitalsied":"30532", "tested":"429526"}
    country_classes[scraper.country_name.lower()] = scraper

    # Portugal
    scraper = NovelScraperAuto()
    scraper.country_name = "Portugal"
    scraper.iso_code = "PT"
    scraper.javascript_required = True
    scraper.report_website = "https://covid19.min-saude.pt/ponto-de-situacao-atual-em-portugal/"
    scraper.source_website = "https://esriportugal.maps.arcgis.com/apps/opsdashboard/index.html#/e9dd1dea8d1444b985d38e58076d197a"
    #scraper.training_data = {"cases": "5170", "deaths": "100", "recovered":"43"}
    country_classes[scraper.country_name.lower()] = scraper

    # The Netherlands
    scraper = NovelScraperAuto()
    scraper.country_name = "Netherlands"
    scraper.iso_code = "NL"
    scraper.optimize_min_max_index_ratio = 0.2
    scraper.source_website = "https://www.rivm.nl/nieuws/actuele-informatie-over-coronavirus"
    #scraper.training_data = {"cases": "9762", "deaths": "639", "hospitalised":"2954"}
    country_classes[scraper.country_name.lower()] = scraper

    # Belgium
    scraper = NovelScraperAuto()
    scraper.country_name = "Belgium"
    scraper.iso_code = "BE"
    scraper.optimize_min_max_index_ratio = 0.2
    scraper.source_website = "https://www.info-coronavirus.be/fr/2020/03/24/526-nouvelles-infections-au-covid-19/"
    #scraper.training_data = {"cases": "4269", "deaths": "122", "recovered":"410", "hospitalised":"1859", "intensive_care":"381"}
    country_classes[scraper.country_name.lower()] = scraper


    # Switzerland
    scraper = NovelScraperAuto()
    scraper.country_name = "Switzerland"
    scraper.iso_code = "CH"
    scraper.optimize_min_max_index_ratio = 0.2
    scraper.source_website = "https://www.bag.admin.ch/bag/en/home/krankheiten/ausbrueche-epidemien-pandemien/aktuelle-ausbrueche-epidemien/novel-cov/situation-schweiz-und-international.html"
    #scraper.training_data = {"cases": "13213", "deaths": "235"}
    country_classes[scraper.country_name.lower()] = scraper

    # Austria
    scraper = NovelScraperAuto()
    scraper.country_name = "Austria"
    scraper.iso_code = "AT"
    scraper.optimize_min_max_index_ratio = 0.2
    scraper.website_scroll = 5
    scraper.source_website = "https://www.sozialministerium.at/Informationen-zum-Coronavirus/Neuartiges-Coronavirus-(2019-nCov).html"
    #scraper.training_data = {"cases": "7995", "deaths": "68", "tested":"42750"}
    country_classes[scraper.country_name.lower()] = scraper

    # Russia (RU)
    scraper = NovelScraperAuto()
    scraper.country_name = "Russia"
    scraper.iso_code = "RU"
    scraper.source_website = "https://www.sozialministerium.at/Informationen-zum-Coronavirus/Neuartiges-Coronavirus-(2019-nCov).html"
    country_classes[scraper.country_name.lower()] = scraper

    # Poland (PL)
    scraper = NovelScraperAuto()
    scraper.country_name = "Poland"
    scraper.iso_code = "PL"
    scraper.source_website = "https://www.sozialministerium.at/Informationen-zum-Coronavirus/Neuartiges-Coronavirus-(2019-nCov).html"
    country_classes[scraper.country_name.lower()] = scraper

    # Czech Republic (CZ)
    scraper = NovelScraperAuto()
    scraper.country_name = "Czech-Republic"
    scraper.iso_code = "CZ"
    scraper.source_website = "https://www.sozialministerium.at/Informationen-zum-Coronavirus/Neuartiges-Coronavirus-(2019-nCov).html"
    country_classes[scraper.country_name.lower()] = scraper

    # Romania (RO)
    scraper = NovelScraperAuto()
    scraper.country_name = "Romania"
    scraper.iso_code = "RO"
    scraper.source_website = "https://www.sozialministerium.at/Informationen-zum-Coronavirus/Neuartiges-Coronavirus-(2019-nCov).html"
    country_classes[scraper.country_name.lower()] = scraper
    
    # Belarus (BY)
    scraper = NovelScraperAuto()
    scraper.country_name = "Russia"
    scraper.iso_code = "BY"
    scraper.source_website = "https://www.sozialministerium.at/Informationen-zum-Coronavirus/Neuartiges-Coronavirus-(2019-nCov).html"
    country_classes[scraper.country_name.lower()] = scraper

    # Ukarine (UA) (CoronaCloud)
    scraper = NovelScraperAuto()
    scraper.country_name = "Ukraine"
    scraper.iso_code = "UA"
    scraper.source_website = "https://www.sozialministerium.at/Informationen-zum-Coronavirus/Neuartiges-Coronavirus-(2019-nCov).html"
    country_classes[scraper.country_name.lower()] = scraper

    # Greece (GR) (CoronaCloud)
    scraper = NovelScraperAuto()
    scraper.country_name = "Greece"
    scraper.iso_code = "GR"
    scraper.source_website = "https://www.sozialministerium.at/Informationen-zum-Coronavirus/Neuartiges-Coronavirus-(2019-nCov).html"
    country_classes[scraper.country_name.lower()] = scraper

    # Andorra
    scraper = NovelScraperAuto()
    scraper.country_name = "Andorra"
    scraper.iso_code = "RU"
    scraper.source_website = "https://www.sozialministerium.at/Informationen-zum-Coronavirus/Neuartiges-Coronavirus-(2019-nCov).html"
    country_classes[scraper.country_name.lower()] = scraper

    # Albania
    scraper = NovelScraperAuto()
    scraper.country_name = "Albania"
    scraper.iso_code = "RU"
    scraper.source_website = "https://www.sozialministerium.at/Informationen-zum-Coronavirus/Neuartiges-Coronavirus-(2019-nCov).html"
    country_classes[scraper.country_name.lower()] = scraper

    # Bosnia and Herzegovina
    scraper = NovelScraperAuto()
    scraper.country_name = "Bosnia-and-herzegovina"
    scraper.iso_code = "RU"
    scraper.source_website = "https://www.sozialministerium.at/Informationen-zum-Coronavirus/Neuartiges-Coronavirus-(2019-nCov).html"
    country_classes[scraper.country_name.lower()] = scraper

    # Bulgaria
    scraper = NovelScraperAuto()
    scraper.country_name = "Bulgaria"
    scraper.iso_code = "RU"
    scraper.source_website = "https://www.sozialministerium.at/Informationen-zum-Coronavirus/Neuartiges-Coronavirus-(2019-nCov).html"
    country_classes[scraper.country_name.lower()] = scraper

    # Croatia
    scraper = NovelScraperAuto()
    scraper.country_name = "Croatia"
    scraper.iso_code = "RU"
    scraper.source_website = "https://www.sozialministerium.at/Informationen-zum-Coronavirus/Neuartiges-Coronavirus-(2019-nCov).html"
    country_classes[scraper.country_name.lower()] = scraper

    # Cyprus
    scraper = NovelScraperAuto()
    scraper.country_name = "Cyprus"
    scraper.iso_code = "RU"
    scraper.source_website = "https://www.sozialministerium.at/Informationen-zum-Coronavirus/Neuartiges-Coronavirus-(2019-nCov).html"
    country_classes[scraper.country_name.lower()] = scraper

    # Hungary
    scraper = NovelScraperAuto()
    scraper.country_name = "Hungary"
    scraper.iso_code = "RU"
    scraper.source_website = "https://www.sozialministerium.at/Informationen-zum-Coronavirus/Neuartiges-Coronavirus-(2019-nCov).html"
    country_classes[scraper.country_name.lower()] = scraper

    # Holy-see
    scraper = NovelScraperAuto()
    scraper.country_name = "Holy-see"
    scraper.iso_code = "RU"
    scraper.source_website = "https://www.sozialministerium.at/Informationen-zum-Coronavirus/Neuartiges-Coronavirus-(2019-nCov).html"
    country_classes[scraper.country_name.lower()] = scraper

    # Kosovo
    scraper = NovelScraperAuto()
    scraper.country_name = "Kosovo"
    scraper.iso_code = "RU"
    scraper.source_website = "https://www.sozialministerium.at/Informationen-zum-Coronavirus/Neuartiges-Coronavirus-(2019-nCov).html"
    country_classes[scraper.country_name.lower()] = scraper

    # Liechtenstein
    scraper = NovelScraperAuto()
    scraper.country_name = "Liechtenstein"
    scraper.iso_code = "RU"
    scraper.source_website = "https://www.sozialministerium.at/Informationen-zum-Coronavirus/Neuartiges-Coronavirus-(2019-nCov).html"
    country_classes[scraper.country_name.lower()] = scraper

    # Luxembourg
    scraper = NovelScraperAuto()
    scraper.country_name = "Luxembourg"
    scraper.iso_code = "RU"
    scraper.source_website = "https://www.sozialministerium.at/Informationen-zum-Coronavirus/Neuartiges-Coronavirus-(2019-nCov).html"
    country_classes[scraper.country_name.lower()] = scraper

    # Malta
    scraper = NovelScraperAuto()
    scraper.country_name = "Malta"
    scraper.iso_code = "RU"
    scraper.source_website = "https://www.sozialministerium.at/Informationen-zum-Coronavirus/Neuartiges-Coronavirus-(2019-nCov).html"
    country_classes[scraper.country_name.lower()] = scraper

    # Moldova
    scraper = NovelScraperAuto()
    scraper.country_name = "Moldova"
    scraper.iso_code = "RU"
    scraper.source_website = "https://www.sozialministerium.at/Informationen-zum-Coronavirus/Neuartiges-Coronavirus-(2019-nCov).html"
    country_classes[scraper.country_name.lower()] = scraper

    # Monaco
    scraper = NovelScraperAuto()
    scraper.country_name = "Monaco"
    scraper.iso_code = "RU"
    scraper.source_website = "https://www.sozialministerium.at/Informationen-zum-Coronavirus/Neuartiges-Coronavirus-(2019-nCov).html"
    country_classes[scraper.country_name.lower()] = scraper

    # Montenegro
    scraper = NovelScraperAuto()
    scraper.country_name = "Montenegro"
    scraper.iso_code = "RU"
    scraper.source_website = "https://www.sozialministerium.at/Informationen-zum-Coronavirus/Neuartiges-Coronavirus-(2019-nCov).html"
    country_classes[scraper.country_name.lower()] = scraper

    # North Macedonia
    scraper = NovelScraperAuto()
    scraper.country_name = "North-Macedonia"
    scraper.iso_code = "RU"
    scraper.source_website = "https://www.sozialministerium.at/Informationen-zum-Coronavirus/Neuartiges-Coronavirus-(2019-nCov).html"
    country_classes[scraper.country_name.lower()] = scraper

    # San Marino
    scraper = NovelScraperAuto()
    scraper.country_name = "San-Marino"
    scraper.iso_code = "RU"
    scraper.source_website = "https://www.sozialministerium.at/Informationen-zum-Coronavirus/Neuartiges-Coronavirus-(2019-nCov).html"
    country_classes[scraper.country_name.lower()] = scraper

    # Slovenia
    scraper = NovelScraperAuto()
    scraper.country_name = "Slovenia"
    scraper.iso_code = "RU"
    scraper.source_website = "https://www.sozialministerium.at/Informationen-zum-Coronavirus/Neuartiges-Coronavirus-(2019-nCov).html"
    country_classes[scraper.country_name.lower()] = scraper

    # Serbia
    scraper = NovelScraperAuto()
    scraper.country_name = "Serbia"
    scraper.iso_code = "RU"
    scraper.source_website = "https://www.sozialministerium.at/Informationen-zum-Coronavirus/Neuartiges-Coronavirus-(2019-nCov).html"
    country_classes[scraper.country_name.lower()] = scraper

    # Slovakia
    scraper = NovelScraperAuto()
    scraper.country_name = "Slovakia"
    scraper.iso_code = "RU"
    scraper.source_website = "https://www.sozialministerium.at/Informationen-zum-Coronavirus/Neuartiges-Coronavirus-(2019-nCov).html"
    country_classes[scraper.country_name.lower()] = scraper    
    

def init_us_scrapers():
    # Alabama
    scraper = NovelScraperAuto()
    scraper.country_name = "Alabama" 
    scraper.iso_code = "AL"
    scraper.has_covidtracking = True
    country_classes[scraper.country_name.lower()] = scraper

    # Alaska
    scraper = NovelScraperAuto()
    scraper.country_name = "Alaska" 
    scraper.iso_code = "AK"
    scraper.has_covidtracking = True
    country_classes[scraper.country_name.lower()] = scraper
    
    # Arizona
    scraper = NovelScraperAuto()
    scraper.country_name = "Arizona" 
    scraper.iso_code = "AZ"
    scraper.has_covidtracking = True
    country_classes[scraper.country_name.lower()] = scraper

    # Arkansas
    scraper = NovelScraperAuto()
    scraper.country_name = "Arkansas" 
    scraper.iso_code = "AR"
    scraper.has_covidtracking = True
    country_classes[scraper.country_name.lower()] = scraper

    # California
    scraper = NovelScraperAuto()
    scraper.country_name = "California" 
    scraper.iso_code = "CA"
    scraper.has_covidtracking = True
    country_classes[scraper.country_name.lower()] = scraper

    # Colorado
    scraper = NovelScraperAuto()
    scraper.country_name = "Colorado" 
    scraper.iso_code = "CO"
    scraper.has_covidtracking = True
    country_classes[scraper.country_name.lower()] = scraper

    # Conneticut
    scraper = NovelScraperAuto()
    scraper.country_name = "Connecticut" 
    scraper.iso_code = "CT"
    scraper.has_covidtracking = True
    country_classes[scraper.country_name.lower()] = scraper

    # Delaware
    scraper = NovelScraperAuto()
    scraper.country_name = "Delaware" 
    scraper.iso_code = "DE"
    scraper.has_covidtracking = True
    country_classes[scraper.country_name.lower()] = scraper

    # Florida
    scraper = NovelScraperAuto()
    scraper.country_name = "Florida" 
    scraper.iso_code = "FL"
    scraper.has_covidtracking = True
    country_classes[scraper.country_name.lower()] = scraper

    # Georgia
    scraper = NovelScraperAuto()
    scraper.country_name = "Georgia" 
    scraper.iso_code = "GA"
    scraper.has_covidtracking = True
    country_classes[scraper.country_name.lower()] = scraper

    # Hawaii
    scraper = NovelScraperAuto()
    scraper.country_name = "Hawaii" 
    scraper.iso_code = "HI"
    scraper.has_covidtracking = True
    country_classes[scraper.country_name.lower()] = scraper

    # Idaho
    scraper = NovelScraperAuto()
    scraper.country_name = "Idaho" 
    scraper.iso_code = "ID"
    scraper.has_covidtracking = True
    country_classes[scraper.country_name.lower()] = scraper

    # Illinois
    scraper = NovelScraperAuto()
    scraper.country_name = "Illinois" 
    scraper.iso_code = "IL"
    scraper.has_covidtracking = True
    country_classes[scraper.country_name.lower()] = scraper

    # Indiana
    scraper = NovelScraperAuto()
    scraper.country_name = "Indiana" 
    scraper.iso_code = "IN"
    scraper.has_covidtracking = True
    country_classes[scraper.country_name.lower()] = scraper

    # Iowa
    scraper = NovelScraperAuto()
    scraper.country_name = "Iowa" 
    scraper.iso_code = "IA"
    scraper.has_covidtracking = True
    country_classes[scraper.country_name.lower()] = scraper

    # Kansas
    scraper = NovelScraperAuto()
    scraper.country_name = "Kansas" 
    scraper.iso_code = "KS"
    scraper.has_covidtracking = True
    country_classes[scraper.country_name.lower()] = scraper

    # Kentucky
    scraper = NovelScraperAuto()
    scraper.country_name = "Kentucky" 
    scraper.iso_code = "KY"
    scraper.has_covidtracking = True
    country_classes[scraper.country_name.lower()] = scraper

    # Louisiana
    scraper = NovelScraperAuto()
    scraper.country_name = "Louisiana" 
    scraper.iso_code = "LA"
    scraper.has_covidtracking = True
    country_classes[scraper.country_name.lower()] = scraper

    # Maine
    scraper = NovelScraperAuto()
    scraper.country_name = "Maine" 
    scraper.iso_code = "ME"
    scraper.has_covidtracking = True
    country_classes[scraper.country_name.lower()] = scraper

    # Maryland
    scraper = NovelScraperAuto()
    scraper.country_name = "Maryland" 
    scraper.iso_code = "MD"
    scraper.has_covidtracking = True
    country_classes[scraper.country_name.lower()] = scraper

    # Massachusetts
    scraper = NovelScraperAuto()
    scraper.country_name = "Massachusetts" 
    scraper.iso_code = "MA"
    scraper.has_covidtracking = True
    country_classes[scraper.country_name.lower()] = scraper

    # Michigan
    scraper = NovelScraperAuto()
    scraper.country_name = "Michigan" 
    scraper.iso_code = "MI"
    scraper.has_covidtracking = True
    country_classes[scraper.country_name.lower()] = scraper

    # Minnesota
    scraper = NovelScraperAuto()
    scraper.country_name = "Minnesota" 
    scraper.iso_code = "MN"
    scraper.has_covidtracking = True
    country_classes[scraper.country_name.lower()] = scraper

    # Mississippi
    scraper = NovelScraperAuto()
    scraper.country_name = "Mississippi" 
    scraper.iso_code = "MS"
    scraper.has_covidtracking = True
    country_classes[scraper.country_name.lower()] = scraper

    # Missouri
    scraper = NovelScraperAuto()
    scraper.country_name = "Missouri" 
    scraper.iso_code = "MO"
    scraper.has_covidtracking = True
    country_classes[scraper.country_name.lower()] = scraper

    # Montana
    scraper = NovelScraperAuto()
    scraper.country_name = "Montana" 
    scraper.iso_code = "MT"
    scraper.has_covidtracking = True
    country_classes[scraper.country_name.lower()] = scraper

    # Nebraska
    scraper = NovelScraperAuto()
    scraper.country_name = "Nebraska" 
    scraper.iso_code = "NE"
    scraper.has_covidtracking = True
    country_classes[scraper.country_name.lower()] = scraper

    # Nevada
    scraper = NovelScraperAuto()
    scraper.country_name = "Nevada" 
    scraper.iso_code = "NV"
    scraper.has_covidtracking = True
    country_classes[scraper.country_name.lower()] = scraper

    # New Hampshire
    scraper = NovelScraperAuto()
    scraper.country_name = "New-Hampshire" 
    scraper.iso_code = "NH"
    scraper.has_covidtracking = True
    country_classes[scraper.country_name.lower()] = scraper

    # New Jersey
    scraper = NovelScraperAuto()
    scraper.country_name = "New-Jersey" 
    scraper.iso_code = "NJ"
    scraper.has_covidtracking = True
    country_classes[scraper.country_name.lower()] = scraper

    # New Mexico
    scraper = NovelScraperAuto()
    scraper.country_name = "New-Mexico" 
    scraper.iso_code = "NM"
    scraper.has_covidtracking = True
    country_classes[scraper.country_name.lower()] = scraper

    # New York
    scraper = NovelScraperAuto()
    scraper.country_name = "New-York" 
    scraper.iso_code = "NY"
    scraper.has_covidtracking = True
    country_classes[scraper.country_name.lower()] = scraper

    # North Carolina
    scraper = NovelScraperAuto()
    scraper.country_name = "North-Carolina" 
    scraper.iso_code = "NC"
    scraper.has_covidtracking = True
    country_classes[scraper.country_name.lower()] = scraper

    # North Dakota
    scraper = NovelScraperAuto()
    scraper.country_name = "North-Dakota" 
    scraper.iso_code = "ND"
    scraper.has_covidtracking = True
    country_classes[scraper.country_name.lower()] = scraper

    # Ohio
    scraper = NovelScraperAuto()
    scraper.country_name = "Ohio" 
    scraper.iso_code = "OH"
    scraper.has_covidtracking = True
    country_classes[scraper.country_name.lower()] = scraper

    # Oklahoma
    scraper = NovelScraperAuto()
    scraper.country_name = "Oklahoma" 
    scraper.iso_code = "OK"
    scraper.has_covidtracking = True
    country_classes[scraper.country_name.lower()] = scraper

    # Oregon
    scraper = NovelScraperAuto()
    scraper.country_name = "Oregon" 
    scraper.iso_code = "OR"
    scraper.has_covidtracking = True
    country_classes[scraper.country_name.lower()] = scraper

    # Pennsylvania
    scraper = NovelScraperAuto()
    scraper.country_name = "Pennsylvania" 
    scraper.iso_code = "PA"
    scraper.has_covidtracking = True
    country_classes[scraper.country_name.lower()] = scraper

    # Rhode Island
    scraper = NovelScraperAuto()
    scraper.country_name = "Rhode-Island" 
    scraper.iso_code = "RI"
    scraper.has_covidtracking = True
    country_classes[scraper.country_name.lower()] = scraper

    # South Carlonia
    scraper = NovelScraperAuto()
    scraper.country_name = "South-Carolina" 
    scraper.iso_code = "SC"
    scraper.has_covidtracking = True
    country_classes[scraper.country_name.lower()] = scraper

    # South Dakota
    scraper = NovelScraperAuto()
    scraper.country_name = "South-Dakota" 
    scraper.iso_code = "SD"
    scraper.has_covidtracking = True
    country_classes[scraper.country_name.lower()] = scraper

    # Tennessee
    scraper = NovelScraperAuto()
    scraper.country_name = "Tennessee" 
    scraper.iso_code = "TN"
    scraper.has_covidtracking = True
    country_classes[scraper.country_name.lower()] = scraper

    # Texas
    scraper = NovelScraperAuto()
    scraper.country_name = "Texas" 
    scraper.iso_code = "TX"
    scraper.has_covidtracking = True
    country_classes[scraper.country_name.lower()] = scraper

    # Utah
    scraper = NovelScraperAuto()
    scraper.country_name = "Utah" 
    scraper.iso_code = "UT"
    scraper.has_covidtracking = True
    country_classes[scraper.country_name.lower()] = scraper

    # Vermont
    scraper = NovelScraperAuto()
    scraper.country_name = "Vermont" 
    scraper.iso_code = "VT"
    scraper.has_covidtracking = True
    country_classes[scraper.country_name.lower()] = scraper

    # Virginia
    scraper = NovelScraperAuto()
    scraper.country_name = "Virginia" 
    scraper.iso_code = "VA"
    scraper.has_covidtracking = True
    country_classes[scraper.country_name.lower()] = scraper

    # Washington
    scraper = NovelScraperAuto()
    scraper.country_name = "Washington" 
    scraper.iso_code = "WA"
    scraper.has_covidtracking = True
    country_classes[scraper.country_name.lower()] = scraper

    # West Virginia
    scraper = NovelScraperAuto()
    scraper.country_name = "West-Virginia" 
    scraper.iso_code = "WV"
    scraper.has_covidtracking = True
    country_classes[scraper.country_name.lower()] = scraper

    # Wisconsin
    scraper = NovelScraperAuto()
    scraper.country_name = "Wisconsin" 
    scraper.iso_code = "WI"
    scraper.has_covidtracking = True
    country_classes[scraper.country_name.lower()] = scraper

    # Wyoming
    scraper = NovelScraperAuto()
    scraper.country_name = "Wyoming" 
    scraper.iso_code = "WY"
    scraper.has_covidtracking = True
    country_classes[scraper.country_name.lower()] = scraper

    # District of Colombia
    scraper = NovelScraperAuto()
    scraper.country_name = "District-of-Columbia" 
    scraper.iso_code = "DC"
    scraper.has_covidtracking = True
    country_classes[scraper.country_name.lower()] = scraper

    # American Samoa
    scraper = NovelScraperAuto()
    scraper.country_name = "American-Samoa" 
    scraper.iso_code = "AS"
    scraper.has_covidtracking = True
    country_classes[scraper.country_name.lower()] = scraper

    # Guam
    scraper = NovelScraperAuto()
    scraper.country_name = "Guam" 
    scraper.iso_code = "GU"
    scraper.has_covidtracking = True
    country_classes[scraper.country_name.lower()] = scraper

    # Northern Mariana Islands
    scraper = NovelScraperAuto()
    scraper.country_name = "Northern-Mariana-Islands" 
    scraper.iso_code = "MP"
    scraper.has_covidtracking = True
    country_classes[scraper.country_name.lower()] = scraper

    # Puerto Rico
    scraper = NovelScraperAuto()
    scraper.country_name = "Puerto-Rico" 
    scraper.iso_code = "PR"
    scraper.has_covidtracking = True
    country_classes[scraper.country_name.lower()] = scraper

    # US Virgin Islands
    scraper = NovelScraperAuto()
    scraper.country_name = "US-Virgin-Islands" 
    scraper.iso_code = "VI"
    scraper.has_covidtracking = True
    country_classes[scraper.country_name.lower()] = scraper

def add_command(triggers : list, function, commands=commands):
    """Add a command to the global players dictionary"""
    if isinstance(triggers, str):
        commands[triggers] = function
    else:
        for trigger in triggers:
            commands[trigger] = function

def add_scheduled_command(command: str, time: datetime):
    scheduled_commands.append([command, time])

def parse(input_list : list) -> dict:
    """Parse the flags of a written line into dictionary representing the flags

    The outputted dict is in the form of {FLAG:value, ...}, where value is
    Union[str, int, list]. Note that the preceeding '-' is removed from flag dict key. 
    The default arguments (with no flag, connecting directly to the command) are stored under
    the flag 'default'
    """
    flags = {}
    #Combine items marked in "" into one item
    new_input_list = []
    combine = False
    for i in input_list:
        if i.startswith("\""):
            new_input_list.append(i + " ")
            combine = True
        elif i.endswith("\""):
            combine = False
            new_input_list[-1] += i + " "
        else:
            if combine:
                new_input_list[-1] += i + " "
            else:
                new_input_list.append(i)

    input_list = new_input_list
        
    if len(input_list) > 1:
        i = 1
        while i < len(input_list) and not (input_list[i][0] == '-' and input_list[i][1].isalpha()):
            flags.setdefault("default", [])
            if isinstance(input_list[i], str):
                if input_list[i].startswith("\""):
                    input_list[i] = input_list[i][1:-2]
                else:
                    input_list[i] = input_list[i].lower()
            flags["default"].append(input_list[i])
            i += 1
        flag = ''
        for value in input_list[i:]:
            if value[0] == '-':
                flag = value[1:]
                flags[flag] = []
            else:
                flags[flag].append(value)

    for flag, args in flags.items():
        if len(args) == 0: 
            flags[flag] = None
        elif len(args) == 1: 
            flags[flag] = args[0]

    return flags

ENABLE_EXTERNAL_COMMANDS = True

def time_is_approximate_equal(time1: datetime.datetime, time2: datetime.datetime):
    allowed_offset = 2
    seconds1 = time1.hour*3600 + time1.minute*60 + time1.second
    seconds2 = time2.hour*3600 + time2.minute*60 + time2.second
    if (seconds1 + allowed_offset) > seconds2 and (seconds1 - allowed_offset) < seconds2:
        return True
    return False

class SchedulingThread(Thread):
    def __init__(self, queue, flags, args=(), kwargs=None):
        Thread.__init__(self, args=(), kwargs=None)
        self.commands = {}
        self.queue = queue

    def run(self):
        add_command(["scrape", "sc"], lambda: cmd_scrape(country_classes, self.flags, discord_bot), self.commands)
        add_command(["screenshot", "ss"], lambda: cmd_screenshot(country_classes, self.flags, discord_bot), self.commands)
        while True:
            # Scheduling
            timenow = datetime.datetime.now()
            for command in scheduled_commands:
                if time_is_approximate_equal(command[1], timenow):
                    #Execute command
                    command_list = command[0].split()
                    self.flags = parse(command_list)
                    print("{}: Executing scheduled command: {}".format(command[1], command[0]))
                    self.commands[command_list[0]]()
            time.sleep(2)
            # Go through external commands
            while not self.queue.empty():
                command = self.queue.get()
                command_list = command.split()
                self.flags = parse(command_list)
                print("Executing external command: {}".format(command))
                self.commands[command_list[0]]()

def main():
    flags = {}
    t = datetime.datetime(year=2020, month=1, day=1, hour=13, minute=14, second=0)
    add_scheduled_command("scrape latvia", t)

    add_command(["scrape", "sc"], lambda: cmd_scrape(country_classes, flags, discord_bot))
    add_command(["train", "tr"], lambda: cmd_train(country_classes, flags, discord_bot))
    add_command(["screenshot", "ss"], lambda: cmd_screenshot(country_classes, flags, discord_bot))
    add_command(["chat", "ch"], lambda: cmd_discord_chat(country_classes, flags, discord_bot))
    add_command(["help", "h"], lambda: cmd_help(country_classes, flags))
    add_command(["exit", "close"], lambda: cmd_exit(country_classes, flags, discord_bot))

    init_europe_scrapers()
    init_us_scrapers()
    command_queue = queue.Queue()

    scheduling_thread = SchedulingThread(command_queue, flags)
    scheduling_thread.start()

    # Start discord bot
    if (DISCORD_BOT_ENABLED):
        print("Starting the Investigator Discord Bot")
        discord_bot.set_command_queue(command_queue)
        discord_bot.start()
        time.sleep(5)
        print("Bot started")

    # Main input loop. Grab input, parse and execute command
    while True:
        input_list = input("\nnvlscrpr: ").split()
        flags = parse(input_list)
        #scheduling_thread.queue.put("scrape latvia")
        if len(input_list) > 0:
            command = input_list[0]
            if command in commands:
                commands[command]()
            else:
                print("The command was not recognized. Type 'help' for a list of commands")
        else:
            print("The command was not recognized. Type 'help' for a list of commands")