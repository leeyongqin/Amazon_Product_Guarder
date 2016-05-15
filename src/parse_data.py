#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
from lxml import etree
import Queue
import time

uk_Queue = Queue.Queue()
de_Queue = Queue.Queue()
fr_Queue = Queue.Queue()
es_Queue = Queue.Queue()
it_Queue = Queue.Queue()


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


def parse_data(raw_info_list=None, country=None):
    # Try to get sku, asin, url_index, url_offer
    product = Product()
    header = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
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
        # print 'Raw Info Failed'

    # Try to get http data from website
    for i in range(3):
        while True:
            try:
                requests_index = requests.get(url_index, header)
                requests_offer = requests.get(url_offer, header)
                if requests_index.status_code == 200 and requests_offer.status_code == 200:
                    html_index = etree.HTML(requests_index.text)
                    html_offer = etree.HTML(requests_offer.text)
                    product.status = 'Found'
                    break

                elif requests_index.status_code == 404:
                    print '%s:%s' % (product.sku, requests_index.status_code)
                    product.status = 'Not Found'
                    return False
                print '%s:%s' % (product.sku, requests_index.status_code)
                # time.sleep(1)
            except Exception, e:
                print "Exception:%s" %e
                time.sleep(1)
                pass
        break

    # process html data got from website
    # Title
    try:
        product.title = html_index.xpath("//*[@id='productTitle']")
        if product.title:
            product.title = product.title[0].text.strip()
        else:
            product.title = html_index.xpath("//*[@id='btAsinTitle']/span")
            if product.title:
                product.title = product.title[0].text.strip()
            else:
                product.title = "★★★No Title★★★"
    except:
        product.title = "★★★No Title★★★"

    # Brand
    try:
        product.brand = html_index.xpath("//*/a[@id='brand']")
        if product.brand:
            product.brand = product.brand[0].text.strip()
        else:
            product.brand = html_index.xpath("//*/div[@class='buying']/span/a")
            if product.brand:
                product.brand = product.brand[0].text.strip()
            else:
                product.brand = "★★★No Brand★★★"
    except:
        product.brand = "★★★No Brand★★★"

    # Price
    if country == 'it':
        try:
            product.price = html_index.xpath("//*[@id='priceblock_ourprice']")
            if product.price:
                product.price = product.price[0].text.strip()
            else:
                product.price = html_index.xpath("//*[@class='priceLarge']")
                if product.price:
                    product.price = product.price[0].text.strip()
                else:
                    product.price = "No Price"
        except:
            product.price = "No Price"
    else:
        try:
            product.price = html_index.xpath("//*[@id='priceblock_ourprice']")
            if product.price:
                product.price = product.price[0].text.strip()
            else:
                product.price = html_index.xpath("//*[@class='priceLarge']")
                if product.price:
                    product.price = product.price[0].text.strip()
                else:
                    product.price = "★★★No Price★★★"
        except :
            product.price = "★★★No Price★★★"

    # Availability
    try:
        product.availability = html_index.xpath("//*/div[@id='availability']/span")
        if product.availability:
            product.availability = product.availability[0].text.strip()
        else:
            product.availability = html_index.xpath("//*[@class='availGreen']")
            if product.availability:
                product.availability = product.availability[0].text.strip()
            else:
                product.availability = "★★★No Availability★★★"
    except:
        product.availability = "★★★No Availability★★★"

    # Buy Box
    if country == 'it':
        try:
            product.buy_box = html_index.xpath("//*/div[@id='merchant-info']/b/a")
            if product.buy_box:
                product.buy_box = product.buy_box[0].text.strip()
            else:
                product.buy_box = html_index.xpath("//*/div[@class='buying']/b/a")
                if product.buy_box:
                    product.buy_box = product.buy_box[0].text.strip()
                else:
                    product.buy_box = "★★★No buy_box★★★"
        except:
            product.buy_box = "★★★No buy_box★★★"
    else:
        try:
            product.buy_box = html_index.xpath("//*/div[@id='merchant-info']/a")
            if product.buy_box:
                product.buy_box = product.buy_box[0].text.strip()
            else:
                product.buy_box = html_index.xpath("//*/div[@class='buying']/b/a")
                if product.buy_box:
                    product.buy_box = product.buy_box[0].text.strip()
                else:
                    product.buy_box = "★★★No buy_box★★★"
        except :
            product.buy_box = "★★★No buy_box★★★"

    # Offer List Info
    # check if negative reviews exist in left column
    reviews_left_list = []
    try:
        reviews_left = html_index.xpath("//*[@id='revMHRL']//*[@class='a-icon-alt']")
        if reviews_left:
            pass
        else:
            reviews_left = html_index.xpath("//*[@id='revMHRL']//*[@class='mt4 ttl']/span[1]/span[1]")
            if reviews_left:
                pass
        for i in reviews_left:
            reviews_left_list.append(i.text[0:1].strip())
    except:
        print 'Can not Find Reviews in the Left Columns'
    # print reviews_left_list
    # Whether Sum of Five Star and Four Star Exceed 8

    # Five Star
    try:
        five_star = html_index.xpath("//*/tr[@class='a-histogram-row'][1]/td[3]/a")
        if five_star:
            five_star = five_star[0].text.replace('%', '').replace(',', '')
        else:
            five_star = html_index.xpath("//*/div[@class='fl histoRowfive clearboth'][1]/a/div[3]")
            if five_star:
                five_star = five_star[0].text.replace('%', '').replace(',', '')
            else:
                five_star = "0"
    except:
        five_star = "0"

    # Four Star
    try:
        four_star = html_index.xpath("//*/tr[@class='a-histogram-row'][2]/td[3]/a")
        if four_star:
            four_star = four_star[0].text.replace('%', '').replace(',', '')
        else:
            four_star = html_index.xpath("//*/div[@class='fl histoRowfour clearboth'][1]/a/div[3]")
            if four_star:
                four_star = four_star[0].text.replace('%', '').replace(',', '')
            else:
                four_star = "0"
    except IndexError:
        four_star = "0"

    # Three Star
    try:
        three_star = html_index.xpath("//*/tr[@class='a-histogram-row'][3]/td[3]/a")
        if three_star:
            three_star = three_star[0].text.replace('%', '').replace(',', '')
        else:
            three_star = html_index.xpath("//*/div[@class='fl histoRowthree clearboth'][1]/a/div[3]")
            if three_star:
                three_star = three_star[0].text.replace('%', '').replace(',', '')
            else:
                three_star = "0"
    except IndexError:
        three_star = "0"

    # Two Star
    try:
        two_star = html_index.xpath("//*/tr[@class='a-histogram-row'][4]/td[3]/a")
        if two_star:
            two_star = two_star[0].text.replace('%', '').replace(',', '')
        else:
            two_star = html_index.xpath("//*/div[@class='fl histoRowtwo clearboth'][1]/a/div[3]")
            if two_star:
                two_star = two_star[0].text.replace('%', '').replace(',', '')
            else:
                two_star = "0"
    except IndexError:
        two_star = "0"

    # One Star
    try:
        one_star = html_index.xpath("//*/tr[@class='a-histogram-row'][5]/td[3]/a")
        if one_star:
            one_star = one_star[0].text.replace('%', '').replace(',', '')
        else:
            one_star = html_index.xpath("//*/div[@class='fl histoRowone clearboth'][1]/a/div[3]")
            if one_star:
                one_star = one_star[0].text.replace('%', '').replace(',', '')
            else:
                one_star = "0"
    except IndexError:
        one_star = "0"

    # print [five_star, four_star, three_star, two_star, one_star]
    # Process Negative Reviews
    negative_exist_in_left = ("1" in reviews_left_list or "2" in reviews_left_list or "3" in reviews_left_list)
    reviews_num_exceed_8 = ((int(five_star.replace('.', '')) + int(four_star.replace('.', ''))) > 8)
    # print negative_exist_in_left, reviews_num_exceed_8
    if negative_exist_in_left and reviews_num_exceed_8:
        product.exist_negative_review = 'Exist negative review'
    else:
        product.exist_negative_review = 'No negative review'

    # Offer List
    # process html data got from website
    # process offer list
    try:
        offer_stand = html_offer.xpath("//*[@class='a-row a-spacing-mini olpOffer']/div[2]/div/span/text()")
        offer_name = html_offer.xpath("//*[@class='a-row a-spacing-mini olpOffer']/div[3]/h3/span/a/text()")
    except:
        print "Get Offer List Failed"

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

    # Return Info
    result = (product.sku, product.brand, product.price,
           product.buy_box, product.availability,
           product.exist_negative_review, product.exist_new_offer)

    if country == 'uk':
        uk_Queue.put(result)
    elif country == 'de':
        de_Queue.put(result)
    elif country == 'fr':
        fr_Queue.put(result)
    elif country == 'es':
        es_Queue.put(result)
    elif country == 'it':
        it_Queue.put(result)
    return True



