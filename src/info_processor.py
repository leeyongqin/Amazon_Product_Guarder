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
    single_sku_info = list()
    for i in xrange(table.nrows):
        sku, asin = table.row_values(i)[0], table.row_values(i)[1]
        if country == 'de':
            url_index = ''
            url_offer = ''
        elif country == 'us':
            url_index = ''
            url_offer = ''
        single_sku_info = [sku, asin, url_index, url_offer]
        raw_info_list.append(single_sku_info)
    return raw_info_list
info_process()

