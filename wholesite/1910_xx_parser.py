#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
parse products by category

21.10 - changes with encoding = line 32
22.10 - random num if product_id doesn't exist
"""

import re
import lxml.html
import urllib
import csv
from lxml.html import fromstring
import time
import random

SLEEP = 2
domain = 'http://www.chemistwarehouse.com.au/'
count_ = {'added': 0,
          'errors': 0}

def parser(url):
    ''' item parser for each product '''
    results = []
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

    for image in doc.cssselect('a.product_img_enlarge'):
        i = image.get('href')
        image = '%s%s' % (domain, i)
        urllib.urlretrieve(image, filename='img/%s.jpg' % product_id)
        results.append(image)

    fp_name = '%s.jpg' % product_id
    results.append(fp_name)
    writer = csv.writer(open('results.csv', 'ab+'), delimiter=';', quotechar='"')
    writer.writerow(results)
    print '[OK] Product: %s' % product_id
    count_['added'] += 1
    print


def main():
    ''' Read from list of categories '''
    reader = csv.reader(open('categories.csv', 'rb'), delimiter=';', quotechar='"')
    for row in reader:
        category_url = row[0]
        # category_url = 'page.html'
        c = urllib.urlopen(category_url)
        data = c.read()
        time.sleep(SLEEP)

        p_lst = []
        pages = re.findall('href\=\"(category\.asp\?id\=(\d+)\&page\=(\d+)\&perPage\=120)\"[>]', data)
        if pages:
            for p in pages:
                p_lst.append(int(p[2]))

            end = max(p_lst) + 1

            for x in range(1, end):
                page = '%scategory.asp?id=%s&page=%s&perPage=120' % (domain, p[1], x)
                c1 = urllib.urlopen(page)
                time.sleep(SLEEP)
                data = c1.read()
                doc = lxml.html.document_fromstring(data)
                for uri in doc.cssselect('div.productName_row a'):
                    url = '%s%s' % (domain, uri.get('href'))
                    print url
                    parser(url)
                    time.sleep(SLEEP)
        else:
            print '[*] Less than 120 products on a page'
            doc = lxml.html.document_fromstring(data)
            for uri in doc.cssselect('div.productName_row a'):
                url = '%s%s' % (domain, uri.get('href'))
                print url
                parser(url)
                time.sleep(SLEEP)
        print count_


if __name__ == "__main__":
    main()