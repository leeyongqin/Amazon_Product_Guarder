#!/usr/bin/python
# -*- coding: UTF-8 -*-

import xlrd


def verify_country():
    pass

"""
sku = raw_info_list[0]
asin = raw_info_list[1]
url_index = raw_info_list[2]
url_offer = raw_info_list[3]
"""


def info_process(country=None):
    if country:
        country = country.lower()
    try:
        fin = xlrd.open_workbook("sku.xls")
        table = fin.sheet_by_index(0)
    except IOError:
        print "No such file or directory: 'sku.xls'"
        exit()
    raw_info_list = list()
    for i in xrange(table.nrows):
        sku, asin = table.row_values(i)[0], table.row_values(i)[1]
        # Europe
        if country == 'de':
            url_index = 'http://www.amazon.de/gp/product/%s/' % asin
            url_offer = 'http://www.amazon.de/gp/offer-listing/%s/' % asin

        elif country == 'fr':
            url_index = 'http://www.amazon.fr/gp/product/%s/' % asin
            url_offer = 'http://www.amazon.fr/gp/offer-listing/%s/' % asin

        elif country == 'uk':
            url_index = 'http://www.amazon.co.uk/gp/product/%s/' % asin
            url_offer = 'http://www.amazon.co.uk/gp/offer-listing/%s/' % asin

        elif country == 'es':
            url_index = 'http://www.amazon.es/gp/product/%s/' % asin
            url_offer = 'http://www.amazon.es/gp/offer-listing/%s/' % asin

        elif country == 'it':
            url_index = 'http://www.amazon.it/gp/product/%s/' % asin
            url_offer = 'http://www.amazon.it/gp/offer-listing/%s/' % asin

        # North America
        elif country == 'us':
            url_index = 'http://www.amazon.com/gp/product/%s/' % asin
            url_offer = 'http://www.amazon.com/gp/offer-listing/%s/' % asin

        elif country == 'ca':
            url_index = 'http://www.amazon.ca/gp/product/%s/' % asin
            url_offer = 'http://www.amazon.ca/gp/offer-listing/%s/' % asin

        # Asia
        elif country == 'jp':
            url_index = 'http://www.amazon.co.jp/gp/product/%s/' % asin
            url_offer = 'http://www.amazon.co.jp/gp/offer-listing/%s/' % asin

        elif country == 'cn':
            url_index = 'http://www.amazon.cn/gp/product/%s/' % asin
            url_offer = 'http://www.amazon.cn/gp/offer-listing/%s/' % asin
        else:
            url_index = None
            url_offer = None

        single_sku_info = [sku, asin, url_index, url_offer]
        if sku != '' or asin != '':
            raw_info_list.append(single_sku_info)
    return raw_info_list

