# This script generate sitemap.xml from csv list of urls

import pandas as pd
import os
import datetime
import pytz
from lxml import etree


# Url source filename
#csv scheme: url, priority, visitors
SOURCE_FILENAME = "example_url_list.csv"

# XML Namespaces
XMLNS_URL = "http://www.sitemaps.org/schemas/sitemap/0.9"
XMLNSXSI_URL = "http://www.w3.org/2001/XMLSchema-instance"


# Generated date
GENERATED_TIME = datetime.datetime.now(pytz.utc).isoformat()

# full file location
SCRIPT_URL = os.path.dirname(os.path.abspath(__file__))

# default priority uses if priority value not specified in report file
DEFAULT_PRIORITY="0.8"
DEFAULT_CHANGEFREQ="weekly"

REPORT_COLUMNS = [
    "url",
    "priority",
    "visitors"
]


# Read file and create list of urls
def get_urls_dataframe(filename):
    dataframe = pd.read_csv("{}/{}".format(SCRIPT_URL, filename), header=None, names=REPORT_COLUMNS)
    # fill nan vaues to default for priority, and 0 for visitors 
    dataframe[REPORT_COLUMNS[1]] = dataframe[REPORT_COLUMNS[1]].fillna(DEFAULT_PRIORITY)
    dataframe[REPORT_COLUMNS[2]] = dataframe[REPORT_COLUMNS[2]].fillna(0)
    return dataframe

def urls_dataframe_to_array(data):
    return data.to_numpy()

# helper function for fast create
def create_SubElement(_parent,_tag,_text=None):
    result = etree.SubElement(_parent,_tag)
    result.text = _text
    return result

# Create new sitemap file with header
def create_sitemap_body(urls_array):
    nsmap = {None: XMLNS_URL, "xsi": XMLNSXSI_URL}
    xml = etree.Element('urlset', nsmap=nsmap)
    
    for url in urls_array:
        url_tag = etree.Element("url")
        
        loc_tag        = create_SubElement(url_tag, "loc", url[0])
        priority_tag   = create_SubElement(url_tag, "priority", url[1])
        changefreq_tag = create_SubElement(url_tag, "changefreq", DEFAULT_CHANGEFREQ)
        lastmod_tag    = create_SubElement(url_tag, "lastmod", GENERATED_TIME)

        # url_tag.append(loc_tag)
        xml.append(url_tag)
    
    return etree.tostring(xml, encoding='utf-8', xml_declaration=True, pretty_print=True)

def create_sitemap_file(urls_array):
    body = create_sitemap_body(urls_array)
    file = open("sitemap-test.xml", "w")
    file.write(body)
    file.close()

data = get_urls_dataframe(SOURCE_FILENAME)
create_sitemap_file(urls_dataframe_to_array(data))
