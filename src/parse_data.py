#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
from lxml import etree
import Queue
import time

uk_Queue = Queue.Queue()
de_Queue = Queue.Queue()


class Product(object):
    def __init__(self):
        self.status = None
        self.sku = None
        self.asin = None
        self.title = None
        self.buy_box = None
        self.brand = None
        self.price = None
        self.availability = None
        self.exist_new_offer = False
        self.exist_negative_review = None

    def __unicode__(self):
        return 'SKU: %s' % self.sku


def parse_data(raw_info_list=None):
    # Try to get sku, asin, url_index, url_offer
    product = Product()
    header = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0 Iceweasel/38.8.0',
        'Accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9, * / *;q = 0.8',
        'Accept - Encoding': 'gzip, deflate',
        'Accept - Language': 'zh - CN, zh;q = 0.8, en - US;q = 0.5, en;q = 0.3',
    }
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
                requests_index = requests.get(url_index, header, timeout=3)
                print requests_index.status_code
                if requests_index.status_code == 200:
                    html_index = etree.HTML(requests_index.content)
                    product.status = 'Found'
                else:
                    print 'Can not find this product: %s' % product.sku
                    product.status = 'Not Found'
                requests_offer = requests.get(url_offer, header, timeout=3)
                html_offer =etree.HTML(requests_offer.content)
                # print "Get Html Data from Website Succeed!"
            except:
                html_index = None
                html_offer = None
                print "Get Html Data Failed, trying.."
                continue
            break
        break

    # process html data got from website
    # title, brand, price, availability, buy_box
    try:
        product.title = html_index.xpath("//*[@id='productTitle'] | //*[@id='btAsinTitle']/span")[0].text.strip()
    except IndexError:
        product.title = "★★★No Title★★★"
        pass

    try:
        product.brand = html_index.xpath("//*/a[@id='brand'] | //*/div[@class='buying']/span/a")[0].text.strip()
    except IndexError:
        product.brand = "★★★No Brand★★★"
        pass

    try:
        product.price = html_index.xpath("//*[@id='priceblock_ourprice'] | //*/td/b[@class='priceLarge']")[0].text.strip()
    except IndexError:
        product.price = "★★★No Price★★★"
        pass

    try:
        product.availability = html_index.xpath("//*/div[@id='availability']/span | //*/span[@class='availGreen']")[
            0].text.strip()
    except IndexError:
        product.availability = "★★★No Availability★★★"
        pass

    try:
        product.buy_box = html_index.xpath("//*/div[@id='merchant-info']/a | //*/div[@class='buying']/b/a")[0].text.strip()
    except IndexError:
        product.buy_box = "★★★No buy_box★★★"
        pass

    # check if negative reviews exist in left column
    reviews_left = html_index.xpath(
        "//*[@id='revMHRL']//*[@class='a-icon-alt'] | //*[@id='revMHRL']//*[@class='mt4 ttl']/span[1]/span[1]")

    # negative review in left column
    try:
        five_star = html_index.xpath(
            "//*/tr[@class='a-histogram-row'][1]/td[3]/a | //*/div[@class='fl histoRowfive clearboth'][1]/a/div[3]")[
            0].text.replace('%', '')
    except IndexError:
        five_star = "0"
        pass
    try:
        four_star = html_index.xpath(
            "//*/tr[@class='a-histogram-row'][2]/td[3]/a | //*/div[@class='fl histoRowfour clearboth'][1]/a/div[3]")[
            0].text.replace('%', '')
    except IndexError:
        four_star = "0"
        pass
    try:
        three_star = html_index.xpath(
            "//*/tr[@class='a-histogram-row'][3]/td[3]/a | //*/div[@class='fl histoRowthree clearboth'][1]/a/div[3]")[
            0].text.replace('%', '')
    except IndexError:
        three_star = "0"
        pass
    try:
        two_star = html_index.xpath(
            "//*/tr[@class='a-histogram-row'][4]/td[3]/a | //*/div[@class='fl histoRowtwo clearboth'][1]/a/div[3]")[
            0].text.replace('%', '')
    except IndexError:
        two_star = "0"
        pass
    try:
        one_star = html_index.xpath(
            "//*/tr[@class='a-histogram-row'][5]/td[3]/a | //*/div[@class='fl histoRowone clearboth'][1]/a/div[3]")[
            0].text.replace('%', '')
    except IndexError:
        one_star = "0"
        pass

    reviews_left_list = list()
    for i in reviews_left:
        reviews_left_list.append(i.text[0:1].strip())
    negative_exist_in_left = "1" in reviews_left_list or "2" in reviews_left_list or "3" in reviews_left_list
    reviews_num_exceed_8 = (int(five_star.replace('.', '')) + int(four_star.replace('.', ''))) > 8
    if negative_exist_in_left and reviews_num_exceed_8:
        product.exist_new_offer = 'Exist negative review'
        # print u"★★★★★WARNING: Negative review exist in left column★★★★★★"
    else:
        product.exist_negative_review = 'No negative review'

    # process html data got from website
    # process offer list
    try:
        offer_stand = html_offer.xpath("//*[@class='a-row a-spacing-mini olpOffer']/div[2]/div/span/text()")
        offer_name = html_offer.xpath("//*[@class='a-row a-spacing-mini olpOffer']/div[3]/h3/span/a/text()")
    except Exception:
        print "Get Offer List Failed"

    new_offer = list()
    own_account = list()
    new_offer_num = 0
    own_account_num = 0
    for i in offer_stand:
        stand = i.replace('\n', '').replace(' ', '')
        if stand in ['Neu']:
            new_offer_num += 1

    for i in offer_name:
        offer = i.replace(' ', '')
        if offer in ['JEDirectDE']:
            own_account_num += 1

    if new_offer_num == own_account_num:
        product.exist_new_offer = 'No other Offer'
    else:
        product.exist_new_offer = 'Exist other Offer'

    result = (product.sku, product.asin, product.status, product.brand, product.price,
           product.buy_box, product.availability,
           product.exist_negative_review, product.exist_new_offer)

    uk_Queue.put(result)
    return result




