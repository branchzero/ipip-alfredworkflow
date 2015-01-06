# coding=utf-8

import urllib2
import json
from xml.etree.ElementTree import Element, SubElement
from xml.etree import ElementTree
from xml.dom import minidom
import hashlib
import sys
import re
import codecs

# Replace Token Info
token = ""
if token == "":
    api_url = "http://freeapi.ipip.net/"
    free_api = 1
else:
    api_url = "http://api.ipip.net/ip/search?token=" + token + "&ip="
    free_api = 0

if sys.stdout.encoding is None:  
    sys.stdout = codecs.getwriter("UTF-8")(sys.stdout)

def generate_feedback(ip, title, subtitle):
    items = Element('items')
    uid = hashlib.md5(ip).hexdigest()
    arg = title
    item = SubElement(items, 'item', {'uid': uid, 'arg': arg})
    element_item_title = SubElement(item, 'title')
    element_item_title.text = title
    element_item_subtitle = SubElement(item, 'subtitle')
    element_item_subtitle.text = subtitle
    element_item_icon = SubElement(item, 'icon')
    element_item_icon.text = "icon.png"

    rough_string = ElementTree.tostring(items, 'utf-8')
    #print rough_string
    print minidom.parseString(rough_string).toprettyxml(indent="    ")

rx = re.compile(r'^([1]?\d\d?|2[0-4]\d|25[0-5])\.([1]?\d\d?|2[0-4]\d|25[0-5])\.([1]?\d\d?|2[0-4]\d|25[0-5])\.([1]?\d\d?|2[0-4]\d|25[0-5])$')
#ip = sys.argv[1]
ip = u'{query}'

if rx.match(ip):

    f = urllib2.urlopen(api_url + ip)
    #print f.read()

    js = f.read()
    #print js
    result = json.loads(js)
    # return code: 0: success, 1: failed
    #code result["code"]
    extra = ""
    if free_api == 0 :
        if 'location' in result:
            extra = "(%s, %s)" % (result['location']['latitude'], result['location']['longitude'])
        result = result["data"]

    country = result[0]
    province = result[1]
    city = result[2]
    if result[3] == "":
        isp = "<No carrier info>"
    else:
        isp = result[3]

    title = "%s %s %s" % (country, province, city)
    subtitle = "%s %s" % (isp, extra)
else:
    title = "Invalid IP Address"
    subtitle = "Please input a valid address"

generate_feedback(ip, title, subtitle)
