from novelscraper import *
from manual_scrapers import *

country_classes = {}
country_aliases = {}
country_aliases_reverse = {}
country_aliases_extended = {}
country_aliases_extended_reverse = {}

def init_europe_scrapers():
    """ Initiate the various country classes """
    group_country_classes = {}

    # Nordic countries:
    # Norway
    scraper = NovelScraperAuto()
    scraper.country_name = "Norway"
    scraper.province_name = "Norway" 
    scraper.iso_code = "NO"
    scraper.javascript_required = True
    scraper.has_auto = True
    scraper.source_website = "https://www.vg.no/spesial/2020/corona/"
    scraper.optimize_min_max_index_ratio = 0.1
    scraper.website_height = 1200
    #scraper.training_data = {"cases": "3752", "deaths":"19", "tested":"78036", "hospitalised": "302", "intensive_care":"76"}
    group_country_classes[scraper.get_index_name()] = scraper

    # Sweden
    scraper = NovelScraperAuto()
    scraper.country_name = "Sweden"
    scraper.province_name = "Sweden"
    scraper.iso_code = "SE"
    scraper.javascript_required = True
    scraper.wait_time = 10
    scraper.optimize_min_max_index_ratio = 0.1
    scraper.website_height = 800
    scraper.has_auto = True
    scraper.source_website = "https://fohm.maps.arcgis.com/apps/opsdashboard/index.html#/68d4537bf2714e63b646c37f152f1392"
    scraper.report_website = "https://www.folkhalsomyndigheten.se/smittskydd-beredskap/utbrott/aktuella-utbrott/covid-19/aktuellt-epidemiologiskt-lage/"
    #scraper.training_data = {"cases": "3046", "deaths": "92", "intensive_care": "209"}
    group_country_classes[scraper.get_index_name()] = scraper

    # Denmark
    # Cases are divided up by regions, can't be parsed with auto
    scraper = NovelScraperDK()
    scraper.scroll_height = 600
    scraper.website_height = 1200
    scraper.has_auto = True
    group_country_classes[scraper.get_index_name()] = scraper

    # Iceland
    scraper = NovelScraperAuto()
    scraper.country_name = "Iceland"
    scraper.province_name = "Iceland"
    scraper.iso_code = "IS"
    scraper.javascript_required = True
    scraper.has_hopkins = True
    scraper.adjust_scraped_deaths_from_sheet = True
    scraper.website_height = 700
    scraper.has_auto = True
    scraper.source_website = "https://e.infogram.com/7327507d-28f5-4e3c-b587-c1680bd790e6?src=embed"
    scraper.report_website = "https://www.covid.is/tolulegar-upplysingar"
    #scraper.training_data = {"cases": "890", "recovered": "97", "hospitalised":"18", "intensive_care":"6", "tested":"13613"}
    group_country_classes[scraper.get_index_name()] = scraper

    # Finland
    scraper = NovelScraperAuto()
    scraper.country_name = "Finland"
    scraper.province_name = "Finland"
    scraper.iso_code = "FI"
    scraper.javascript_required = True
    scraper.has_auto = True
    scraper.source_website = "https://korona.kans.io/"
    #scraper.training_data = {"cases": "1056", "deaths": "7", "recovered": "10"}
    group_country_classes[scraper.get_index_name()] = scraper

    # Estonia
    scraper = NovelScraperAuto()
    scraper.country_name = "Estonia" 
    scraper.province_name = "Estonia" 
    scraper.iso_code = "EE"
    scraper.source_website = "https://www.koroonakaart.ee/en"
    scraper.website_height = 500
    scraper.has_auto = True
    #scraper.training_data = {"cases": "640",  "deaths": "1", "recovered":"20", "tested":"9364", "hospitalised": "48"}
    group_country_classes[scraper.get_index_name()] = scraper

    # Lithuania
    scraper = NovelScraperAuto()
    scraper.country_name = "Lithuania"
    scraper.province_name = "Lithuania" 
    scraper.iso_code = "LI"
    scraper.source_website = "https://sam.lrv.lt/lt/naujienos/koronavirusas"
    scraper.scroll_height= 400
    scraper.website_height = 1200
    scraper.website_width = 1920
    scraper.has_auto = True
    #scraper.training_data = {"cases": "382",  "deaths": "5", "recovered":"1", "tested":"6900"}
    group_country_classes[scraper.get_index_name()] = scraper

    # Latvia
    scraper = NovelScraperAuto()
    scraper.country_name = "Latvia" 
    scraper.province_name = "Latvia" 
    scraper.iso_code = "LV"
    scraper.source_website = "https://arkartassituacija.gov.lv/"
    scraper.website_height = 1200
    scraper.has_auto = True
    #scraper.training_data = {"cases": "280", "tested":"11702", "hospitalised": "21"}
    group_country_classes[scraper.get_index_name()] = scraper

    # Central Europe
    # The United Kingdom
    scraper = NovelScraperAuto()
    scraper.country_name = "UK"
    scraper.province_name = "UK"
    scraper.iso_code = "GB"
    scraper.javascript_required = True
    scraper.report_link = "https://www.gov.uk/government/publications/covid-19-track-coronavirus-cases"
    scraper.source_website = "https://www.arcgis.com/apps/opsdashboard/index.html#/f94c3c90da5b4e9f9a0b19484dd4bb14"
    #scraper.training_data = {"cases": "17089", "recovered":"135", "deaths": "1019"}
    group_country_classes[scraper.get_index_name()] = scraper

    # Ireland
    scraper = NovelScraperAuto()
    scraper.country_name = "Ireland"
    scraper.province_name = "Ireland"
    scraper.iso_code = "IE"
    scraper.javascript_required = True
    scraper.source_website = "https://www.gov.ie/en/news/7e0924-latest-updates-on-covid-19-coronavirus/"
    scraper.scroll_height = 500
    #scraper.training_data = {"cases": "2415", "deaths": "36"}
    group_country_classes[scraper.get_index_name()] = scraper

    # Germany
    scraper = NovelScraperAuto()
    scraper.country_name = "Germany"
    scraper.province_name = "Germany"
    scraper.iso_code = "DE"
    scraper.javascript_required = True
    scraper.source_website = "https://interaktiv.morgenpost.de/corona-virus-karte-infektionen-deutschland-weltweit-teaser/"
    #scraper.training_data = {"cases": "54268", "deaths": "398", "recovered":"3781"}
    group_country_classes[scraper.get_index_name()] = scraper

    # France
    # Can't scrape images. Should probably do a custom one
    scraper = NovelScraperAuto()
    scraper.country_name = "France"
    scraper.province_name = "France"
    scraper.iso_code = "FR"
    scraper.javascript_required = True
    scraper.source_website = "https://www.santepubliquefrance.fr/maladies-et-traumatismes/maladies-et-infections-respiratoires/infection-a-coronavirus/articles/infection-au-nouveau-coronavirus-sars-cov-2-covid-19-france-et-monde"
    scraper.scroll_height = 1700
    #scraper.training_data = {"cases": "54268", "deaths": "398", "recovered":"3781"}
    group_country_classes[scraper.get_index_name()] = scraper

    # Spain
    scraper = NovelScraperAuto()
    scraper.country_name = "Spain"
    scraper.province_name = "Spain"
    scraper.iso_code = "ES"
    scraper.javascript_required = True
    scraper.optimize_min_max_index_ratio = 0.1
    scraper.source_website = "https://www.rtve.es/noticias/20200328/mapa-del-coronavirus-espana/2004681.shtml"
    #scraper.training_data = {"cases": "73235", "deaths": "5982", "recovered":"12285", "intensive_care":"4575"}
    group_country_classes[scraper.get_index_name()] = scraper

    # Italy
    scraper = NovelScraperAuto()
    scraper.country_name = "Italy"
    scraper.province_name = "Italy"
    scraper.iso_code = "IT"
    scraper.javascript_required = True
    scraper.optimize_min_max_index_ratio = 0.05
    scraper.source_website = "https://datastudio.google.com/u/0/reporting/91350339-2c97-49b5-92b8-965996530f00/page/RdlHB"
    #scraper.training_data = {"cases": "92472", "deaths": "10023", "recovered":"12384", "intensive_care":"3856", "hospitalsied":"30532", "tested":"429526"}
    group_country_classes[scraper.get_index_name()] = scraper

    # Portugal
    scraper = NovelScraperAuto()
    scraper.country_name = "Portugal"
    scraper.province_name = "Portugal"
    scraper.iso_code = "PT"
    scraper.javascript_required = True
    scraper.report_website = "https://covid19.min-saude.pt/ponto-de-situacao-atual-em-portugal/"
    # Mobile https://esriportugal.maps.arcgis.com/apps/opsdashboard/index.html#/e9dd1dea8d1444b985d38e58076d197a
    scraper.source_website = "https://esriportugal.maps.arcgis.com/apps/opsdashboard/index.html#/acf023da9a0b4f9dbb2332c13f635829"
    #scraper.training_data = {"cases": "5170", "deaths": "100", "recovered":"43"}
    group_country_classes[scraper.get_index_name()] = scraper

    # The Netherlands
    scraper = NovelScraperAuto()
    scraper.country_name = "Netherlands"
    scraper.province_name = "Netherlands"
    scraper.iso_code = "NL"
    scraper.optimize_min_max_index_ratio = 0.2
    scraper.source_website = "https://www.rivm.nl/nieuws/actuele-informatie-over-coronavirus"
    #scraper.training_data = {"cases": "9762", "deaths": "639", "hospitalised":"2954"}
    group_country_classes[scraper.get_index_name()] = scraper

    # Bad, all the stuff are on different links. Best is https://datastudio.google.com/embed/reporting/c14a5cfc-cab7-4812-848c-0369173148ab/page/tpRKB
    scraper = NovelScraperAuto()
    scraper.country_name = "Belgium"
    scraper.province_name = "Belgium"
    scraper.iso_code = "BE"
    scraper.optimize_min_max_index_ratio = 0.2
    #scraper.source_website = "https://www.info-coronavirus.be/fr/2020/03/24/526-nouvelles-infections-au-covid-19/"
    #scraper.training_data = {"cases": "4269", "deaths": "122", "recovered":"410", "hospitalised":"1859", "intensive_care":"381"}
    group_country_classes[scraper.get_index_name()] = scraper

    # Switzerland
    scraper = NovelScraperAuto()
    scraper.country_name = "Switzerland"
    scraper.province_name = "Switzerland"
    scraper.iso_code = "CH"
    scraper.optimize_min_max_index_ratio = 0.2
    scraper.source_website = "https://www.bag.admin.ch/bag/en/home/krankheiten/ausbrueche-epidemien-pandemien/aktuelle-ausbrueche-epidemien/novel-cov/situation-schweiz-und-international.html"
    scraper.scroll_height = 300
    #scraper.training_data = {"cases": "13213", "deaths": "235"}
    group_country_classes[scraper.get_index_name()] = scraper

    # Austria
    scraper = NovelScraperAuto()
    scraper.country_name = "Austria"
    scraper.province_name = "Austria"
    scraper.iso_code = "AT"
    scraper.optimize_min_max_index_ratio = 0.2
    scraper.website_height = 3000
    scraper.website_width = 1800
    scraper.scroll_height = 200
    scraper.source_website = "https://www.sozialministerium.at/Informationen-zum-Coronavirus/Neuartiges-Coronavirus-(2019-nCov).html"
    #scraper.training_data = {"cases": "7995", "deaths": "68", "tested":"42750"}
    group_country_classes[scraper.get_index_name()] = scraper

    # Russia (RU)
    scraper = NovelScraperAuto()
    scraper.country_name = "Russia"
    scraper.province_name = "Russia"
    scraper.iso_code = "RU"
    scraper.source_website = "https://www.interfax.ru/chronicle/novyj-koronavirus-v-kitae.html&usg=ALkJrhhW6tC7Wqpa7vbQeaYKlTlQ8ZkIBA"
    group_country_classes[scraper.get_index_name()] = scraper

    # Poland (PL)
    scraper = NovelScraperAuto()
    scraper.country_name = "Poland"
    scraper.province_name = "Poland"
    scraper.iso_code = "PL"
    #scraper.source_website = "https://koronawirusunas.pl/"
    scraper.source_website = "https://pokazwirusa.pl/?fbclid=IwAR1bkCIad8H4F-2-2WgYv2pbrleRWgPeUCVDu97X-C2DV0GPfiqlxx7_z9s"
    group_country_classes[scraper.get_index_name()] = scraper

    # Czech Republic (CZ)
    scraper = NovelScraperAuto()
    scraper.country_name = "Czech-Republic"
    scraper.province_name = "Czech-Republic"
    scraper.iso_code = "CZ"
    scraper.source_website = "https://onemocneni-aktualne.mzcr.cz/covid-19"
    group_country_classes[scraper.get_index_name()] = scraper

    # Romania (RO)
    scraper = NovelScraperAuto()
    scraper.country_name = "Romania"
    scraper.province_name = "Romania"
    scraper.iso_code = "RO"
    # Secondary https://instnsp.maps.arcgis.com/apps/opsdashboard/index.html#/5eced796595b4ee585bcdba03e30c127
    scraper.source_website = "https://covid19.geo-spatial.org/dashboard/main"
    group_country_classes[scraper.get_index_name()] = scraper
    
    # Belarus (BY)
    scraper = NovelScraperAuto()
    scraper.country_name = "Belarus"
    scraper.province_name = "Belarus"
    scraper.iso_code = "BY"
    scraper.source_website = "http://stopcovid.belta.by/"
    scraper.has_auto = True
    scraper.javascript_required = True
    scraper.combine_text_numbers = False
    group_country_classes[scraper.get_index_name()] = scraper

    # Ukarine (UA) (CoronaCloud)
    scraper = NovelScraperAuto()
    scraper.country_name = "Ukraine"
    scraper.province_name = "Ukraine"
    scraper.iso_code = "UA"
    #scraper.source_website = "https://www.sozialministerium.at/Informationen-zum-Coronavirus/Neuartiges-Coronavirus-(2019-nCov).html"
    group_country_classes[scraper.get_index_name()] = scraper

    # Greece (GR) (CoronaCloud)
    scraper = NovelScraperAuto()
    scraper.country_name = "Greece"
    scraper.province_name = "Greece"
    scraper.iso_code = "GR"
    #scraper.source_website = "https://www.sozialministerium.at/Informationen-zum-Coronavirus/Neuartiges-Coronavirus-(2019-nCov).html"
    group_country_classes[scraper.get_index_name()] = scraper

    # Andorra
    scraper = NovelScraperAuto()
    scraper.country_name = "Andorra"
    scraper.province_name = "Andorra"
    scraper.iso_code = "AD"
    scraper.report_website = "https://www.govern.ad/coronavirus"
    scraper.source_website = "https://www.govern.ad/covid/taula.php"
    scraper.website_height = 200
    scraper.javascript_required = True
    scraper.has_auto = True
    group_country_classes[scraper.get_index_name()] = scraper 

    # Albania
    scraper = NovelScraperAuto()
    scraper.country_name = "Albania"
    scraper.province_name = "Albania"
    scraper.iso_code = "AL"
    scraper.source_website = "https://coronavirus.al/statistika/"
    scraper.has_hopkins = True
    scraper.javascript_required = True
    scraper.has_auto = True
    group_country_classes[scraper.get_index_name()] = scraper

    # Bosnia and Herzegovina
    scraper = NovelScraperAuto()
    scraper.country_name = "Bosnia-and-Herzegovina"
    scraper.province_name = "Bosnia-and-Herzegovina"
    scraper.iso_code = "BA"
    scraper.report_website = "https://www.klix.ba/koronavirus-u-bih"
    scraper.source_website = "https://www.klix.ba/corona/"
    scraper.has_auto = True
    scraper.javascript_required = True
    group_country_classes[scraper.get_index_name()] = scraper

    # Bulgaria
    scraper = NovelScraperAuto()
    scraper.country_name = "Bulgaria"
    scraper.province_name = "Bulgaria"
    scraper.iso_code = "BG"
    scraper.source_website = "https://www.mh.government.bg/bg/informaciya-za-grazhdani/potvrdeni-sluchai-na-koronavirus-na-teritoriyata-na-r-blgariya/"
    scraper.has_auto = True
    group_country_classes[scraper.get_index_name()] = scraper

    # Croatia
    scraper = NovelScraperAuto()
    scraper.country_name = "Croatia"
    scraper.province_name = "Croatia"
    scraper.iso_code = "HR"
    scraper.source_website = "https://www.koronavirus.hr/"
    scraper.has_auto = True
    group_country_classes[scraper.get_index_name()] = scraper

    # Cyprus
    scraper = NovelScraperAuto()
    scraper.country_name = "Cyprus"
    scraper.province_name = "Cyprus"
    scraper.iso_code = "CY"
    #scraper.source_website = "https://www.sozialministerium.at/Informationen-zum-Coronavirus/Neuartiges-Coronavirus-(2019-nCov).html"
    group_country_classes[scraper.get_index_name()] = scraper

    # Hungary
    scraper = NovelScraperHU()
    group_country_classes[scraper.get_index_name()] = scraper

    # Holy-see
    scraper = NovelScraperAuto()
    scraper.country_name = "Holy-see"
    scraper.province_name = "Holy-see"
    scraper.iso_code = "VA"
    #scraper.source_website = "https://www.sozialministerium.at/Informationen-zum-Coronavirus/Neuartiges-Coronavirus-(2019-nCov).html"
    group_country_classes[scraper.get_index_name()] = scraper

    # Kosovo
    scraper = NovelScraperAuto()
    scraper.country_name = "Kosovo"
    scraper.province_name = "Kosovo"
    scraper.iso_code = "XK"
    scraper.source_website = "https://kosova.health/en/"
    scraper.scroll_height = 600
    scraper.has_auto = True
    group_country_classes[scraper.get_index_name()] = scraper

    # Liechtenstein
    scraper = NovelScraperAuto()
    scraper.country_name = "Liechtenstein"
    scraper.province_name = "Liechtenstein"
    scraper.iso_code = "LI"
    #scraper.source_website = "https://www.sozialministerium.at/Informationen-zum-Coronavirus/Neuartiges-Coronavirus-(2019-nCov).html"
    group_country_classes[scraper.get_index_name()] = scraper

    # Luxembourg
    scraper = NovelScraperAuto()
    scraper.country_name = "Luxembourg"
    scraper.province_name = "Luxembourg"
    scraper.iso_code = "LU"
    scraper.source_website = "https://msan.gouvernement.lu/en/dossiers/2020/corona-virus.html"
    scraper.has_auto = True
    scraper.scroll_height = 300
    group_country_classes[scraper.get_index_name()] = scraper

    # Malta
    scraper = NovelScraperAuto()
    scraper.country_name = "Malta"
    scraper.province_name = "Malta"
    scraper.iso_code = "MT"
    scraper.report_website = "https://www.maltatoday.com.mt/"
    scraper.source_website = "https://e.infogram.com/ca2bde8e-e60d-49a1-8faa-5beab8e542ab?parent_url=https%3A%2F%2Fwww.maltatoday.com.mt%2F&src=embed#async_embed"
    scraper.javascript_required = True
    scraper.has_auto = True
    scraper.website_height = 300
    scraper.combine_text_numbers = False
    scraper.overwrite_model_surrounding_numbers = True
    group_country_classes[scraper.get_index_name()] = scraper

    # Moldova
    scraper = NovelScraperAuto()
    scraper.country_name = "Moldova"
    scraper.province_name = "Moldova"
    scraper.iso_code = "MD"
    #scraper.source_website = "https://www.sozialministerium.at/Informationen-zum-Coronavirus/Neuartiges-Coronavirus-(2019-nCov).html"
    group_country_classes[scraper.get_index_name()] = scraper

    # Monaco
    scraper = NovelScraperAuto()
    scraper.country_name = "Monaco"
    scraper.province_name = "Monaco"
    scraper.iso_code = "MC"
    #scraper.source_website = "https://www.sozialministerium.at/Informationen-zum-Coronavirus/Neuartiges-Coronavirus-(2019-nCov).html"
    group_country_classes[scraper.get_index_name()] = scraper

    # Montenegro
    scraper = NovelScraperAuto()
    scraper.country_name = "Montenegro"
    scraper.province_name = "Montenegro"
    scraper.iso_code = "ME"
    #scraper.source_website = "https://www.sozialministerium.at/Informationen-zum-Coronavirus/Neuartiges-Coronavirus-(2019-nCov).html"
    group_country_classes[scraper.get_index_name()] = scraper

    # North Macedonia
    scraper = NovelScraperAuto()
    scraper.country_name = "North-Macedonia"
    scraper.province_name = "North-Macedonia"
    scraper.iso_code = "MK"
    #scraper.source_website = "https://www.sozialministerium.at/Informationen-zum-Coronavirus/Neuartiges-Coronavirus-(2019-nCov).html"
    group_country_classes[scraper.get_index_name()] = scraper

    # San Marino
    scraper = NovelScraperAuto()
    scraper.country_name = "San-Marino"
    scraper.province_name = "San-Marino"
    scraper.iso_code = "SM"
    #scraper.source_website = "https://www.sozialministerium.at/Informationen-zum-Coronavirus/Neuartiges-Coronavirus-(2019-nCov).html"
    group_country_classes[scraper.get_index_name()] = scraper

    # Slovenia
    scraper = NovelScraperAuto()
    scraper.country_name = "Slovenia"
    scraper.province_name = "Slovenia"
    scraper.iso_code = "SI"
    #scraper.source_website = "https://www.sozialministerium.at/Informationen-zum-Coronavirus/Neuartiges-Coronavirus-(2019-nCov).html"
    group_country_classes[scraper.get_index_name()] = scraper

    # Serbia
    scraper = NovelScraperAuto()
    scraper.country_name = "Serbia"
    scraper.province_name = "Serbia"
    scraper.iso_code = "RS"
    scraper.has_auto = True
    scraper.javascript_required = True
    scraper.source_website = "https://covid19.rs/"
    group_country_classes[scraper.get_index_name()] = scraper

    # Slovakia
    scraper = NovelScraperAuto()
    scraper.country_name = "Slovakia"
    scraper.province_name = "Slovakia"
    scraper.iso_code = "SK"
    #scraper.source_website = "https://www.sozialministerium.at/Informationen-zum-Coronavirus/Neuartiges-Coronavirus-(2019-nCov).html"
    group_country_classes[scraper.get_index_name()] = scraper    

    for country_name, scraper in group_country_classes.items(): #Values applied to all countries within this function
        scraper.group_name = "Europe"

    country_classes.update(group_country_classes)

    
def init_us_scrapers():
    group_country_classes = {}

    country_name = "United-States"

    # Alabama
    scraper = NovelScraperAuto()
    scraper.country_name = country_name
    scraper.province_name = "Alabama" 
    scraper.iso_code = "AL"
    scraper.source_website = "https://alpublichealth.maps.arcgis.com/apps/opsdashboard/index.html#/6d2771faa9da4a2786a509d82c8cf0f7"
    group_country_classes[scraper.get_index_name()] = scraper

    # Alaska
    scraper = NovelScraperAuto()
    scraper.country_name = country_name
    scraper.province_name = "Alaska" 
    scraper.iso_code = "AK"
    scraper.javascript_required = True
    scraper.report_website = "https://coronavirus-response-alaska-dhss.hub.arcgis.com/"
    scraper.source_website = "https://www.arcgis.com/apps/opsdashboard/index.html#/83c63cfec8b24397bdf359f49b11f218"
    scraper.scroll_height = 800
    scraper.website_height = 1200
    group_country_classes[scraper.get_index_name()] = scraper
    
    # Arizona
    scraper = NovelScraperAuto()
    scraper.country_name = country_name
    scraper.province_name = "Arizona" 
    scraper.iso_code = "AZ"
    scraper.javascript_required = True
    scraper.report_website = "https://www.azdhs.gov/preparedness/epidemiology-disease-control/infectious-disease-epidemiology/index.php#novel-coronavirus-home"
    scraper.source_website = "https://tableau.azdhs.gov/views/UpdatedCOVIDdashboardV3/Story1?:embed=y&:showVizHome=no&:host_url=https%3A%2F%2Ftableau.azdhs.gov%2F&:embed_code_version=3&:tabs=no&:toolbar=no&:showAppBanner=false&:display_spinner=no&iframeSizedToWindow=true&:loadOrderID=0"
    group_country_classes[scraper.get_index_name()] = scraper

    # Arkansas
    scraper = NovelScraperAuto()
    scraper.country_name = country_name
    scraper.province_name = "Arkansas" 
    scraper.iso_code = "AR"
    scraper.report_website = "https://www.healthy.arkansas.gov/programs-services/topics/novel-coronavirus"
    scraper.source_website = "https://adem.maps.arcgis.com/apps/opsdashboard/index.html#/f533ac8a8b6040e5896b05b47b17a647"
    scraper.javascript_required = True
    group_country_classes[scraper.get_index_name()] = scraper

    # California (not official source but updates faster)
    scraper = NovelScraperAuto()
    scraper.country_name = country_name
    scraper.province_name = "California" 
    scraper.iso_code = "CA"
    scraper.source_website = "https://www.latimes.com/projects/california-coronavirus-cases-tracking-outbreak/"
    group_country_classes[scraper.get_index_name()] = scraper

    # Colorado
    scraper = NovelScraperAuto()
    scraper.country_name = country_name
    scraper.province_name = "Colorado" 
    scraper.iso_code = "CO"
    scraper.report_website = "https://covid19.colorado.gov/case-data"
    scraper.source_website = "https://public.tableau.com/views/COVID19_CaseSummary_TP/COVID-19CaseSummary-TP?:embed=y&:showVizHome=no&:host_url=https%3A%2F%2Fpublic.tableau.com%2F&:embed_code_version=3&:tabs=no&:toolbar=yes&:animate_transition=yes&:display_static_image=no&:display_spinner=no&:display_overlay=yes&:display_count=yes&publish=yes&:loadOrderID=0"
    group_country_classes[scraper.get_index_name()] = scraper

    # Conneticut (primary source is in pdf, ugh)
    scraper = NovelScraperAuto()
    scraper.country_name = country_name
    scraper.province_name = "Connecticut" 
    scraper.iso_code = "CT"
    scraper.has_auto = True
    scraper.source_website = "https://www.nytimes.com/interactive/2020/us/connecticut-coronavirus-cases.html"
    #scraper.source_website = https://portal.ct.gov/coronavirus
    group_country_classes[scraper.get_index_name()] = scraper

    # Delaware
    scraper = NovelScraperAuto()
    scraper.country_name = country_name
    scraper.province_name = "Delaware" 
    scraper.iso_code = "DE"
    scraper.report_website = "https://coronavirus.delaware.gov/"
    scraper.source_website = "https://dshs.maps.arcgis.com/apps/opsdashboard/index.html#/f2b22615feeb442aa2975900f8f2d4a1"
    group_country_classes[scraper.get_index_name()] = scraper

    # Florida
    scraper = NovelScraperAuto()
    scraper.country_name = country_name
    scraper.province_name = "Florida" 
    scraper.iso_code = "FL"
    scraper.javascript_required = True
    scraper.has_auto = True
    scraper.wait_time = 14
    scraper.source_website = "https://fdoh.maps.arcgis.com/apps/opsdashboard/index.html#/8d0de33f260d444c852a615dc7837c86"
    group_country_classes[scraper.get_index_name()] = scraper

    # Georgia
    scraper = NovelScraperAuto()
    scraper.country_name = country_name
    scraper.province_name = "Georgia" 
    scraper.iso_code = "GA"
    scraper.report_website = "https://dph.georgia.gov/covid-19-daily-status-report"
    scraper.javascript_required = True
    scraper.has_auto = True
    scraper.scroll_height = 200
    scraper.source_website = "https://d20s4vd27d0hk0.cloudfront.net/?initialWidth=746&childId=covid19dashdph&parentTitle=COVID-19%20Daily%20Status%20Report%20%7C%20Georgia%20Department%20of%20Public%20Health&parentUrl=https%3A%2F%2Fdph.georgia.gov%2Fcovid-19-daily-status-report"
    group_country_classes[scraper.get_index_name()] = scraper

    # Hawaii
    scraper = NovelScraperAuto()
    scraper.country_name = country_name
    scraper.province_name = "Hawaii" 
    scraper.iso_code = "HI"
    scraper.source_website = "https://health.hawaii.gov/coronavirusdisease2019/"
    group_country_classes[scraper.get_index_name()] = scraper

    # Idaho
    scraper = NovelScraperAuto()
    scraper.country_name = country_name
    scraper.province_name = "Idaho" 
    scraper.iso_code = "ID"
    scraper.javascript_required = True
    scraper.report_website = "https://coronavirus.idaho.gov/"
    scraper.source_website = "https://public.tableau.com/profile/idaho.division.of.public.health#!/vizhome/DPHIdahoCOVID-19Dashboard_V2/DPHCOVID19Dashboard2"
    group_country_classes[scraper.get_index_name()] = scraper

    # Illinois
    scraper = NovelScraperAuto()
    scraper.country_name = country_name
    scraper.province_name = "Illinois" 
    scraper.iso_code = "IL"
    scraper.source_website = "http://www.dph.illinois.gov/topics-services/diseases-and-conditions/diseases-a-z-list/coronavirus"
    scraper.scroll_height = 200
    scraper.javascript_required = True
    scraper.has_auto = True
    group_country_classes[scraper.get_index_name()] = scraper

    # Indiana
    scraper = NovelScraperAuto()
    scraper.country_name = country_name
    scraper.province_name = "Indiana" 
    scraper.iso_code = "IN"
    scraper.javascript_required = True
    scraper.source_website = "https://coronavirus.in.gov/"
    scraper.scroll_height = 2200
    scraper.website_width = 1500
    group_country_classes[scraper.get_index_name()] = scraper

    # Iowa (No deaths reported here?)
    scraper = NovelScraperAuto()
    scraper.country_name = country_name
    scraper.province_name = "Iowa" 
    scraper.iso_code = "IA"
    #scraper.report_website = https://idph.iowa.gov/Emerging-Health-Issues/Novel-Coronavirus
    scraper.source_website = "https://idph.iowa.gov/Emerging-Health-Issues/Novel-Coronavirus"
    scraper.javascript_required = True
    scraper.wait_time = 7
    scraper.website_height = 1200
    scraper.scroll_height = 200
    group_country_classes[scraper.get_index_name()] = scraper

    # Kansas
    scraper = NovelScraperAuto()
    scraper.country_name = country_name
    scraper.province_name = "Kansas" 
    scraper.iso_code = "KS"
    scraper.source_website = "https://public.tableau.com/profile/kdhe.epidemiology#!/vizhome/COVID-19Data_15851817634470/KSCOVID-19CaseData"
    scraper.javascript_required = True
    group_country_classes[scraper.get_index_name()] = scraper

    # Kentucky
    scraper = NovelScraperAuto()
    scraper.country_name = country_name
    scraper.province_name = "Kentucky" 
    scraper.iso_code = "KY"
    scraper.source_website = "https://govstatus.egov.com/kycovid19"
    group_country_classes[scraper.get_index_name()] = scraper

    # Louisiana
    scraper = NovelScraperAuto()
    scraper.country_name = country_name
    scraper.province_name = "Louisiana" 
    scraper.iso_code = "LA"
    scraper.source_website = "https://www.arcgis.com/apps/opsdashboard/index.html#/69b726e2b82e408f89c3a54f96e8f776"
    scraper.report_website = "http://ldh.la.gov/Coronavirus/"
    scraper.javascript_required = True
    scraper.has_auto = True
    group_country_classes[scraper.get_index_name()] = scraper

    # Maine
    scraper = NovelScraperAuto()
    scraper.country_name = country_name
    scraper.province_name = "Maine" 
    scraper.iso_code = "ME"
    scraper.source_website = "https://www.maine.gov/dhhs/mecdc/infectious-disease/epi/airborne/coronavirus.shtml"
    scraper.scroll_height = 400
    scraper.website_height = 1200
    group_country_classes[scraper.get_index_name()] = scraper

    # Maryland
    scraper = NovelScraperAuto()
    scraper.country_name = country_name
    scraper.province_name = "Maryland" 
    scraper.iso_code = "MD"
    scraper.source_website = "https://maryland.maps.arcgis.com/apps/opsdashboard/index.html#/c34e541dd8b742d993159dbebb094d8b"
    scraper.report_website = "https://coronavirus.maryland.gov/"
    scraper.javascript_required = True
    group_country_classes[scraper.get_index_name()] = scraper

    # Massachusetts
    scraper = NovelScraperAuto()
    scraper.country_name = country_name
    scraper.province_name = "Massachusetts" 
    scraper.iso_code = "MA"
    scraper.source_website = "https://www.mass.gov/info-details/covid-19-cases-quarantine-and-monitoring#covid-19-cases-in-massachusetts-"
    scraper.scroll_height = 900
    scraper.website_height = 1200
    scraper.website_width=1600
    scraper.has_auto = True
    scraper.adjust_scraped_deaths_from_sheet = True
    group_country_classes[scraper.get_index_name()] = scraper

    # Michigan
    scraper = NovelScraperAuto()
    scraper.country_name = country_name
    scraper.province_name = "Michigan" 
    scraper.iso_code = "MI"
    scraper.source_website = "https://www.michigan.gov/coronavirus/0,9753,7-406-98163_98173---,00.html"
    scraper.website_height = 1200
    scraper.scroll_height = 2200
    scraper.has_auto = True
    group_country_classes[scraper.get_index_name()] = scraper

    # Minnesota
    scraper = NovelScraperAuto()
    scraper.country_name = country_name
    scraper.province_name = "Minnesota" 
    scraper.iso_code = "MN"
    scraper.report_website = "https://www.health.state.mn.us/diseases/coronavirus/situation.html"
    scraper.source_website = "https://mndps.maps.arcgis.com/apps/opsdashboard/index.html#/f28f84968c1148129932c3bebb1d3a1a"
    scraper.javascript_required = True
    group_country_classes[scraper.get_index_name()] = scraper

    # Mississippi
    scraper = NovelScraperAuto()
    scraper.country_name = country_name
    scraper.province_name = "Mississippi" 
    scraper.iso_code = "MS"
    scraper.source_website = "https://msdh.ms.gov/msdhsite/_static/14,0,420.html"
    scraper.scroll_height = 1300
    scraper.website_height = 1200
    scraper.javascript_required = True
    group_country_classes[scraper.get_index_name()] = scraper

    # Missouri
    scraper = NovelScraperAuto()
    scraper.country_name = country_name
    scraper.province_name = "Missouri" 
    scraper.iso_code = "MO"
    scraper.source_website = "https://health.mo.gov/living/healthcondiseases/communicable/novel-coronavirus/results.php"
    group_country_classes[scraper.get_index_name()] = scraper

    # Montana
    scraper = NovelScraperAuto()
    scraper.country_name = country_name
    scraper.province_name = "Montana" 
    scraper.iso_code = "MT"
    scraper.source_website = "https://montana.maps.arcgis.com/apps/MapSeries/index.html?appid=7c34f3412536439491adcc2103421d4b"
    scraper.javascript_required = True
    group_country_classes[scraper.get_index_name()] = scraper

    # Nebraska
    scraper = NovelScraperAuto()
    scraper.country_name = country_name
    scraper.province_name = "Nebraska" 
    scraper.iso_code = "NE"
    scraper.source_website = "https://nebraska.maps.arcgis.com/apps/opsdashboard/index.html#/4213f719a45647bc873ffb58783ffef3"
    scraper.javascript_required = True
    group_country_classes[scraper.get_index_name()] = scraper

    # Nevada
    scraper = NovelScraperAuto()
    scraper.country_name = country_name
    scraper.province_name = "Nevada" 
    scraper.iso_code = "NV"
    scraper.source_website = "https://app.powerbigov.us/view?r=eyJrIjoiMjA2ZThiOWUtM2FlNS00MGY5LWFmYjUtNmQwNTQ3Nzg5N2I2IiwidCI6ImU0YTM0MGU2LWI4OWUtNGU2OC04ZWFhLTE1NDRkMjcwMzk4MCJ9"
    scraper.javascript_required = True
    scraper.wait_time = 10
    group_country_classes[scraper.get_index_name()] = scraper

    # New Hampshire
    scraper = NovelScraperAuto()
    scraper.country_name = country_name
    scraper.province_name = "New-Hampshire" 
    scraper.iso_code = "NH"
    scraper.source_website = "https://www.nh.gov/covid19/"
    scraper.scroll_height = 200
    group_country_classes[scraper.get_index_name()] = scraper

    # New Jersey
    scraper = NovelScraperAuto()
    scraper.country_name = country_name
    scraper.province_name = "New-Jersey" 
    scraper.iso_code = "NJ"
    scraper.report_website = "https://covid19.nj.gov/#live-updates"
    scraper.source_website = "https://maps.arcgis.com/apps/opsdashboard/index.html#/ec4bffd48f7e495182226eee7962b422"
    scraper.javascript_required = True
    scraper.has_auto = True
    group_country_classes[scraper.get_index_name()] = scraper

    # New Mexico
    scraper = NovelScraperAuto()
    scraper.country_name = country_name
    scraper.province_name = "New-Mexico" 
    scraper.iso_code = "NM"
    scraper.source_website = "https://cv.nmhealth.org/"
    scraper.scroll_height = 100
    scraper.website_height = 1200
    group_country_classes[scraper.get_index_name()] = scraper

    # New York
    scraper = NovelScraperAuto()
    scraper.country_name = country_name
    scraper.province_name = "New-York"
    scraper.iso_code = "NY"
    scraper.source_website = "https://www.nbcnewyork.com/news/local/how-many-in-tri-state-have-tested-positive-for-coronavirus-here-are-latest-cases-by-the-numbers/2317721/"
    scraper.javascript_required = True
    scraper.has_auto = True
    scraper.scroll_height = 3400
    group_country_classes[scraper.get_index_name()] = scraper

    # North Carolina
    scraper = NovelScraperAuto()
    scraper.country_name = country_name
    scraper.province_name = "North-Carolina" 
    scraper.iso_code = "NC"
    scraper.source_website = "https://www.ncdhhs.gov/divisions/public-health/covid19/covid-19-nc-case-count"
    scraper.scroll_height = 100
    scraper.website_height = 1200
    group_country_classes[scraper.get_index_name()] = scraper

    # North Dakota
    scraper = NovelScraperAuto()
    scraper.country_name = country_name
    scraper.province_name = "North-Dakota" 
    scraper.iso_code = "ND"
    scraper.source_website = "https://www.health.nd.gov/diseases-conditions/coronavirus/north-dakota-coronavirus-cases"
    scraper.website_height = 1200
    scraper.scroll_height = 100
    group_country_classes[scraper.get_index_name()] = scraper

    # Ohio
    scraper = NovelScraperAuto()
    scraper.country_name = country_name
    scraper.province_name = "Ohio" 
    scraper.iso_code = "OH"
    scraper.source_website = "https://coronavirus.ohio.gov/wps/portal/gov/covid-19/home"
    scraper.scroll_height = 600
    group_country_classes[scraper.get_index_name()] = scraper

    # Oklahoma
    scraper = NovelScraperAuto()
    scraper.country_name = country_name
    scraper.province_name = "Oklahoma" 
    scraper.iso_code = "OK"
    scraper.source_website = "https://coronavirus.health.ok.gov/"
    scraper.scroll_height = 500
    scraper.website_width = 1600
    group_country_classes[scraper.get_index_name()] = scraper

    # Oregon
    scraper = NovelScraperAuto()
    scraper.country_name = country_name
    scraper.province_name = "Oregon" 
    scraper.iso_code = "OR"
    scraper.source_website = "https://govstatus.egov.com/OR-OHA-COVID-19"
    scraper.scroll_height = 1000
    scraper.website_width = 1600
    group_country_classes[scraper.get_index_name()] = scraper

    # Pennsylvania
    scraper = NovelScraperAuto()
    scraper.country_name = country_name
    scraper.province_name = "Pennsylvania" 
    scraper.iso_code = "PA"
    scraper.source_website = "https://www.health.pa.gov/topics/disease/coronavirus/Pages/Cases.aspx"
    scraper.scroll_height = 200
    scraper.has_auto = True
    group_country_classes[scraper.get_index_name()] = scraper

    # Rhode Island
    scraper = NovelScraperAuto()
    scraper.country_name = country_name
    scraper.province_name = "Rhode-Island" 
    scraper.iso_code = "RI"
    scraper.source_website = "https://health.ri.gov/data/covid-19/"
    scraper.scroll_height = 300
    scraper.javascript_required = True
    group_country_classes[scraper.get_index_name()] = scraper

    # South Carlonia
    scraper = NovelScraperAuto()
    scraper.country_name = country_name
    scraper.province_name = "South-Carolina" 
    scraper.iso_code = "SC"
    scraper.report_website = "https://scdhec.gov/infectious-diseases/viruses/coronavirus-disease-2019-covid-19/testing-sc-data-covid-19"
    scraper.source_website = "https://sc-dhec.maps.arcgis.com/apps/opsdashboard/index.html#/3732035614af4246877e20c3a496e397"
    scraper.javascript_required = True
    group_country_classes[scraper.get_index_name()] = scraper

    # South Dakota
    scraper = NovelScraperAuto()
    scraper.country_name = country_name
    scraper.province_name = "South-Dakota" 
    scraper.iso_code = "SD"
    scraper.source_website = "https://doh.sd.gov/news/Coronavirus.aspx"
    scraper.scroll_height = 1200
    group_country_classes[scraper.get_index_name()] = scraper

    # Tennessee
    scraper = NovelScraperAuto()
    scraper.country_name = country_name
    scraper.province_name = "Tennessee" 
    scraper.iso_code = "TN"
    scraper.source_website = "https://www.tn.gov/health/cedep/ncov.html"
    scraper.scroll_height = 1150
    scraper.website_height = 1200
    scraper.javascript_required = True
    group_country_classes[scraper.get_index_name()] = scraper

    # Texas
    scraper = NovelScraperAuto()
    scraper.country_name = country_name
    scraper.province_name = "Texas" 
    scraper.iso_code = "TX"
    scraper.source_website = "https://txdshs.maps.arcgis.com/apps/opsdashboard/index.html#/ed483ecd702b4298ab01e8b9cafc8b83"
    scraper.javascript_required = True
    scraper.has_auto = True
    group_country_classes[scraper.get_index_name()] = scraper

    # Utah
    scraper = NovelScraperAuto()
    scraper.country_name = country_name
    scraper.province_name = "Utah" 
    scraper.iso_code = "UT"
    scraper.source_website = "https://coronavirus-dashboard.utah.gov/"
    scraper.javascript_required = True
    group_country_classes[scraper.get_index_name()] = scraper

    # Vermont
    scraper = NovelScraperAuto()
    scraper.country_name = country_name
    scraper.province_name = "Vermont" 
    scraper.iso_code = "VT"
    scraper.source_website = "https://www.nytimes.com/interactive/2020/us/vermont-coronavirus-cases.html"
    scraper.javascript_required = True
    group_country_classes[scraper.get_index_name()] = scraper

    # Virginia
    scraper = NovelScraperAuto()
    scraper.country_name = country_name
    scraper.province_name = "Virginia" 
    scraper.iso_code = "VA"
    scraper.source_website = "https://public.tableau.com/views/VirginiaCOVID-19Dashboard/VirginiaCOVID-19Dashboard?:embed=yes&:display_count=yes&:showVizHome=no&:toolbar=no"
    scraper.javascript_required = True
    group_country_classes[scraper.get_index_name()] = scraper

    # Washington
    scraper = NovelScraperAuto()
    scraper.country_name = country_name
    scraper.province_name = "Washington" 
    scraper.iso_code = "WA"
    scraper.report_website = "https://www.doh.wa.gov/Emergencies/Coronavirus"
    scraper.source_website = "https://msit.powerbi.com/view?r=eyJrIjoiYzQ2YmYxZmEtYjlkNy00YjNkLWEyYTEtNzJmYzU3ZGI1MmZjIiwidCI6IjcyZjk4OGJmLTg2ZjEtNDFhZi05MWFiLTJkN2NkMDExZGI0NyIsImMiOjV9"
    scraper.javascript_required = True
    scraper.has_auto = True
    scraper.wait_time = 10
    group_country_classes[scraper.get_index_name()] = scraper

    # West Virginia
    scraper = NovelScraperAuto()
    scraper.country_name = country_name
    scraper.province_name = "West-Virginia" 
    scraper.iso_code = "WV"
    scraper.report_website = "https://dhhr.wv.gov/COVID-19/Pages/default.aspx"
    scraper.source_website = "https://app.powerbigov.us/view?r=eyJrIjoiMTg3YjRkZTgtNzhlZi00MGJlLTk1MTAtN2ZhOWExZWY4OWYyIiwidCI6IjhhMjZjZjAyLTQzNGEtNDMxZS04Y2FkLTdlYWVmOTdlZjQ4NCJ9"
    scraper.javascript_required = True
    scraper.wait_time = 10
    group_country_classes[scraper.get_index_name()] = scraper

    # Wisconsin
    scraper = NovelScraperAuto()
    scraper.country_name = country_name
    scraper.province_name = "Wisconsin" 
    scraper.iso_code = "WI"
    scraper.source_website = "https://www.dhs.wisconsin.gov/outbreaks/index.htm"
    scraper.javascript_required = True
    scraper.scroll_height = 800
    group_country_classes[scraper.get_index_name()] = scraper

    # Wyoming
    scraper = NovelScraperAuto()
    scraper.country_name = country_name
    scraper.province_name = "Wyoming" 
    scraper.iso_code = "WY"
    scraper.source_website = "https://health.wyo.gov/publichealth/infectious-disease-epidemiology-unit/disease/novel-coronavirus/covid-19-map-and-statistics/"
    scraper.javascript_required = True
    scraper.wait_time = 10
    group_country_classes[scraper.get_index_name()] = scraper

    # District of Colombia
    scraper = NovelScraperAuto()
    scraper.country_name = country_name
    scraper.province_name = "District-of-Columbia" 
    scraper.iso_code = "DC"
    scraper.source_website = "https://coronavirus.dc.gov/page/coronavirus-data"
    group_country_classes[scraper.get_index_name()] = scraper

    # American Samoa
    scraper = NovelScraperAuto()
    scraper.country_name = country_name
    scraper.province_name = "American-Samoa" 
    scraper.iso_code = "AS"
    #scraper.source_website = 
    group_country_classes[scraper.get_index_name()] = scraper

    # Guam
    scraper = NovelScraperAuto()
    scraper.country_name = country_name
    scraper.province_name = "Guam" 
    scraper.iso_code = "GU"
    #scraper.source_website = 
    group_country_classes[scraper.get_index_name()] = scraper

    # Northern Mariana Islands
    scraper = NovelScraperAuto()
    scraper.country_name = country_name
    scraper.province_name = "Northern-Mariana-Islands" 
    scraper.iso_code = "MP"
    scraper.source_website = "https://www.chcc.gov.mp/coronavirusinformation.php"
    scraper.javascript_required = True
    group_country_classes[scraper.get_index_name()] = scraper

    # Puerto Rico
    scraper = NovelScraperAuto()
    scraper.country_name = country_name
    scraper.province_name = "Puerto-Rico" 
    scraper.iso_code = "PR"
    scraper.source_website = "https://estadisticas.pr/en/covid-19"
    scraper.javascript_required = True
    group_country_classes[scraper.get_index_name()] = scraper

    # US Virgin Islands
    scraper = NovelScraperAuto()
    scraper.country_name = country_name
    scraper.province_name = "US-Virgin-Islands" 
    scraper.iso_code = "VI"
    scraper.source_website = "https://doh.vi.gov/covid19usvi"
    scraper.scroll_height = 500
    group_country_classes[scraper.get_index_name()] = scraper

    for country_name, scraper in group_country_classes.items(): #Values applied to all countries within this function
        scraper.group_name = "USA"
        scraper.has_covidtracking = True

    country_classes.update(group_country_classes)

def init_canada_scrapers():
    group_country_classes = {}

    country_name = "Canada"

    # Alberta
    scraper = NovelScraperAuto()
    scraper.country_name = country_name 
    scraper.province_name = "Alberta" 
    scraper.iso_code = "N/A"
    scraper.source_website = "https://covid19stats.alberta.ca/"
    group_country_classes[scraper.get_index_name()] = scraper

    # British Columbia
    scraper = NovelScraperAuto()
    scraper.country_name = country_name 
    scraper.province_name = "British-Columbia" 
    scraper.iso_code = "N/A"
    scraper.source_website = "https://governmentofbc.maps.arcgis.com/apps/opsdashboard/index.html#/11bd9b0303c64373b5680df29e5b5914"
    scraper.has_auto = True
    scraper.javascript_required = True
    scraper.wait_time = 15
    group_country_classes[scraper.get_index_name()] = scraper

    # Manitoba
    scraper = NovelScraperAuto()
    scraper.country_name = country_name 
    scraper.province_name = "Manitoba" 
    scraper.iso_code = "N/A"
    scraper.source_website = "https://www.gov.mb.ca/covid19/updates/index.html"
    scraper.scroll_height = 400
    scraper.has_auto = True
    group_country_classes[scraper.get_index_name()] = scraper

    # New Brunswick
    scraper = NovelScraperAuto()
    scraper.country_name = country_name 
    scraper.province_name = "New-Brunswick" 
    scraper.iso_code = "N/A"
    scraper.source_website = "https://www2.gnb.ca/content/gnb/en/corporate/promo/covid-19/maps_graphs.html"
    scraper.scroll_height = 600
    scraper.has_auto = True
    group_country_classes[scraper.get_index_name()] = scraper

    # Newfoundland and Labrador
    scraper = NovelScraperAuto()
    scraper.country_name = country_name
    scraper.province_name = "Newfoundland-and-Labrador" 
    scraper.iso_code = "N/A"
    scraper.source_website = "https://covid-19-newfoundland-and-labrador-gnl.hub.arcgis.com/"
    scraper.javascript_required = True
    scraper.has_auto = True
    group_country_classes[scraper.get_index_name()] = scraper

    # Nova Scotia
    scraper = NovelScraperAuto()
    scraper.country_name = country_name
    scraper.province_name = "Nova-Scotia" 
    scraper.iso_code = "N/A"
    scraper.source_website = "https://novascotia.ca/coronavirus/data/"
    scraper.javascript_required = True
    scraper.scroll_height = 300
    scraper.has_auto = True
    group_country_classes[scraper.get_index_name()] = scraper

    # Ontario
    scraper = NovelScraperAuto()
    scraper.country_name = country_name
    scraper.province_name = "Ontario" 
    scraper.iso_code = "N/A"
    scraper.source_website = "https://www.ontario.ca/page/2019-novel-coronavirus#2"
    scraper.website_height = 1200
    scraper.scroll_height = 1800
    scraper.javascript_required = True
    scraper.has_auto = True
    group_country_classes[scraper.get_index_name()] = scraper

    # Quebec
    scraper = NovelScraperAuto()
    scraper.country_name = country_name
    scraper.province_name = "Quebec" 
    scraper.iso_code = "N/A"
    scraper.source_website = "https://www.inspq.qc.ca/covid-19/donnees"
    scraper.javascript_required = True
    scraper.has_auto = True
    group_country_classes[scraper.get_index_name()] = scraper

    # Saskatchewan
    scraper = NovelScraperAuto()
    scraper.country_name = country_name
    scraper.province_name = "Saskatchewan" 
    scraper.iso_code = "N/A"
    scraper.source_website = "https://www.saskatchewan.ca/government/health-care-administration-and-provider-resources/treatment-procedures-and-guidelines/emerging-public-health-issues/2019-novel-coronavirus/cases-and-risk-of-covid-19-in-saskatchewan"
    scraper.has_auto = True
    group_country_classes[scraper.get_index_name()] = scraper

    # Yukon
    scraper = NovelScraperAuto()
    scraper.country_name = country_name
    scraper.province_name = "Yukon" 
    scraper.iso_code = "N/A"
    scraper.source_website = "https://yukon.ca/covid-19"
    scraper.has_auto = True
    group_country_classes[scraper.get_index_name()] = scraper

    # Northwest Territories
    scraper = NovelScraperAuto()
    scraper.country_name = country_name
    scraper.province_name = "Northwest-Territories" 
    scraper.iso_code = "N/A"
    scraper.source_website = "https://www.hss.gov.nt.ca/en/services/coronavirus-disease-covid-19"
    scraper.scroll_height = 300
    scraper.has_auto = True
    group_country_classes[scraper.get_index_name()] = scraper

    # Prince Edward Island
    scraper = NovelScraperAuto()
    scraper.country_name = country_name
    scraper.province_name = "Prince-Edward-Island" 
    scraper.iso_code = "N/A"
    scraper.has_auto = True
    scraper.source_website = "https://www.princeedwardisland.ca/en/information/health-and-wellness/pei-covid-19-testing-data"
    group_country_classes[scraper.get_index_name()] = scraper

    # Nunavut (No JH data?)
    scraper = NovelScraperAuto()
    scraper.country_name = country_name
    scraper.province_name = "Nunavut" 
    scraper.iso_code = "N/A"
    scraper.source_website = "https://gov.nu.ca/health/information/covid-19-novel-coronavirus"
    scraper.scroll_height = 300
    scraper.has_auto = True
    group_country_classes[scraper.get_index_name()] = scraper

    for country_name, scraper in group_country_classes.items(): #Values applied to all countries within this function
        scraper.group_name = "Canada"

    country_classes.update(group_country_classes)

def create_country_aliases():
    for country_name, scraper in country_classes.items():
        country_aliases[scraper.province_name.lower()] = country_name

    for country_name, scraper in country_classes.items():
        country_aliases_reverse[country_name] = scraper.province_name.lower()
        country_aliases_extended_reverse[scraper.get_pretty_name()] = scraper.province_name.lower()
        country_aliases_extended_reverse[country_name] = scraper.province_name.lower()


    