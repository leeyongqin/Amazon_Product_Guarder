#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
from lxml import etree


class Product(object):
    def __init__(self):
        self.sku = None
        self.asin = None
        self.title = None
        self.buy_box = None
        self.brand = None
        self.availability = None
        self.exist_new_offer = False
        self.exist_negative_review = None

    def __unicode__(self):
        return 'SKU: %s' % self.sku


def sku_asin_url_processor(file=None):
    pass


def parse_data(raw_info_list):
    # Try to get sku, asin, url_index, url_offer
    product = Product()
    try:
        product.sku = raw_info_list[0]
        product.asin = raw_info_list[1]
        url_index = raw_info_list[2]
        url_offer = raw_info_list[3]
    except IndexError:
        product.sku = None
        product.asin = None
        url_index = None
        url_offer = None
        print 'Raw Info Failed'

    # Try to get http data from website
    for i in range(3):
        while True:
            try:
                requests_index = requests.get(url_index, timeout=3)
                html_index = etree.HTML(requests_index.content)
                requests_offer = requests.get(url_offer, timeout=3)
                html_offer =etree.HTML(requests_offer.content)
                print u"Get Html Data from Website Succeed!"
            except Exception:
                html_index = None
                html_offer = None
                print u"Get Html Data Failed, trying.."
                continue
            break
        break

    # process html data got from website
    # title, brand, price, availability, buy_box
    try:
        product.title = html_index.xpath("//*[@id='productTitle'] | //*[@id='btAsinTitle']/span")[0].text.strip()
    except IndexError:
        product.title = u"★★★No Title★★★"
        pass

    try:
        product.brand = html_index.xpath("//*/a[@id='brand'] | //*/div[@class='buying']/span/a")[0].text.strip()
    except IndexError:
        product.brand = u"★★★No Brand★★★"
        pass

    try:
        product.price = html_index.xpath("//*[@id='priceblock_ourprice'] | //*/td/b[@class='priceLarge']")[0].text.strip()
    except IndexError:
        product.price = u"★★★No Price★★★"
        pass

    try:
        product.availability = html_index.xpath("//*/div[@id='availability']/span | //*/span[@class='availGreen']")[
            0].text.strip()
    except IndexError:
        product.availability = u"★★★No Availability★★★"
        pass

    try:
        product.buy_box = html_index.xpath("//*/div[@id='merchant-info']/a | //*/div[@class='buying']/b/a")[0].text.strip()
    except IndexError:
        product.buy_box = u"★★★No buy_box★★★"
        pass

    # check if negative reviews exist in left column
    reviews_left = html_index.xpath(
        "//*[@id='revMHRL']//*[@class='a-icon-alt'] | //*[@id='revMHRL']//*[@class='mt4 ttl']/span[1]/span[1]")

    # negative review in left column
    try:
        five_star = html_index.xpath(
            "//*/tr[@class='a-histogram-row'][1]/td[3]/a | //*/div[@class='fl histoRowfive clearboth'][1]/a/div[3]")[
            0].text
    except IndexError:
        five_star = "0"
        pass
    try:
        four_star = html_index.xpath(
            "//*/tr[@class='a-histogram-row'][2]/td[3]/a | //*/div[@class='fl histoRowfour clearboth'][1]/a/div[3]")[
            0].text
    except IndexError:
        four_star = "0"
        pass
    try:
        three_star = html_index.xpath(
            "//*/tr[@class='a-histogram-row'][3]/td[3]/a | //*/div[@class='fl histoRowthree clearboth'][1]/a/div[3]")[
            0].text
    except IndexError:
        three_star = "0"
        pass
    try:
        two_star = html_index.xpath(
            "//*/tr[@class='a-histogram-row'][4]/td[3]/a | //*/div[@class='fl histoRowtwo clearboth'][1]/a/div[3]")[
            0].text
    except IndexError:
        two_star = "0"
        pass
    try:
        one_star = html_index.xpath(
            "//*/tr[@class='a-histogram-row'][5]/td[3]/a | //*/div[@class='fl histoRowone clearboth'][1]/a/div[3]")[
            0].text
    except IndexError:
        one_star = "0"
        pass

    reviews_left_list = list()
    for i in reviews_left:
        reviews_left_list.append(i.text[0:1].strip())
    negative_exist_in_left = "1" in reviews_left_list or "2" in reviews_left_list or "3" in reviews_left_list
    reviews_num_exceed_8 = (int(five_star.replace('.', '')) + int(four_star.replace('.', ''))) > 8
    if negative_exist_in_left and reviews_num_exceed_8:
        product.exist_new_offer = True
        print u"★★★★★WARNING: Negative review exist in left column★★★★★★"
    else:
        product.exist_negative_review = False

    # process html data got from website
    # process offer list
    try:
        offer_quality = html_offer.xpath("//*[@class='a-row a-spacing-mini olpOffer']/div[2]/div/span/text()")
        offer_name = html_offer.xpath("//*[@class='a-row a-spacing-mini olpOffer']/div[3]/h3/span/a/text()")
    except Exception:
        print "Get Offer List Failed"

    new_offer = list()
    own_account = list()
    for i in offer_quality:
        quality = i.replace('\n', '').replace(' ', '')
        if quality in  ['Neu']:
            print new_offer.append(quality),

    for i in offer_name:
        offer = i.replace(' ', '')
        if offer in ['JEDirect']:
            own_account.append(offer)

    if len(new_offer) == len(own_account):
        product.exist_new_offer = False
    else:
        product.exist_new_offer = True

    print (product.sku, product.asin, product.title, product.brand, product.price, product.buy_box, product.availability,\
        product.exist_negative_review, product.exist_new_offer)
    return product




