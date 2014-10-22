#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
No. | Name | Catagory | Price | Description (if we can separate them would be perfect) | Pictures
"""

__author__ = 'adubnyak@gmail.com'

import re
import lxml.html
import urllib
import csv
# import xlrd, xlwt
# import time
from lxml.html import fromstring

import random

writer = csv.writer(open('results.csv', 'ab+'), delimiter=';', quotechar='"')
domain = 'http://www.chemistwarehouse.com.au/'
results = []

url = 'page.html'
c = urllib.urlopen(url)
data = c.read()
product_id = re.findall('style\=\"text-align\:left\;.padding\:5px.0\;.color\:\#\d+\"[>]\w+.ID\:.(\d+)[<]', data)
try:
    product_id = product_id[0]
except IndexError:
    product_id = 'NoId_%s' % random.randint(0, 9999)
results.append(product_id)

# name
doc = lxml.html.document_fromstring(data)
for title in doc.cssselect('div.ProductPage_ProductName'):
    name = title.text
    results.append(name.encode('utf-8'))

category = re.findall('[<]b[>]Home[<]\/b[>](.*)[<]\/b', data)
for c in category:
    c_lst = c.split('<b>')
    results.append(c_lst[-1])

for price in doc.cssselect('div.ProductPage_NormalPrice'):
    results.append(price.text)

# description

desc = re.findall('itemprop\=\"description\"[>](.*)[<]\/div[>]', data)
results.append('\n'.join(desc))

    # description = '%s\n' % d


for image in doc.cssselect('a.product_img_enlarge'):
    i = image.get('href')
    image = '%s%s' % (domain, i)
    # urllib.urlretrieve(image, filename='img/%s.jpg' % product_id)
    results.append(image)

fp_name = '%s.jpg' % product_id
results.append(fp_name)
writer.writerow(results)
print '[OK] Product: %s' % product_id
