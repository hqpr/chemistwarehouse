#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
grab all links to categories
http://www.chemistwarehouse.com.au/categories.asp
"""

import re
import lxml.html
import urllib
import csv

url = 'page.html'
writer = csv.writer(open('categories.csv', 'wb+'), delimiter=';', quotechar='"')
c = urllib.urlopen(url)
data = c.read()
match = re.findall('href\=\"category\.asp\?id\=(\d+)\&cname\=(\w+)\".[>](\S+)[<]\/a', data)

for m in match:
    category_url = 'http://www.chemistwarehouse.com.au/category.asp?id=%s%s' % (m[0], '&perPage=120&sortby=')
    name = m[1]
    writer.writerow([category_url, name])

print 'done'