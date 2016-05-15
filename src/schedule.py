#!/usr/bin/python
# -*- coding: UTF-8 -*-

from send_mail import send_mail
from info_processor import info_process
from parse_data import parse_data, uk_Queue, de_Queue, fr_Queue, es_Queue, it_Queue
import threading
import time
import multiprocessing

uk_list = list()
de_list = list()
fr_list = list()
es_list = list()
it_list = list()


def multi_threading():
    process_list = []
    country_list = ['uk']
    for i in xrange(len(country_list)):
        process = multiprocessing.Process(target=schedule, args=(country_list[i], ))
        process.start()
        process_list.append(process)
        time.sleep(2)
    for item in process_list:
        item.join()


def schedule(country=None):
    info = info_process(country)
    thread_list = []
    for item in info:
        thread_name = 'thread_%s_%s' % (country, item[1])
        thread_name = threading.Thread(target=parse_data, args=(item, country))
        thread_name.start()
        # time.sleep(1)
        thread_list.append(thread_name)
    for item in thread_list:
        item.join()

    for i in range(uk_Queue.qsize()):
        uk_temp = uk_Queue.get()
        if uk_temp[1] not in ['JETech', 'Helect'] or uk_temp[3] not in ['JEDirect UK'] or\
                        uk_temp[5] == 'Exist negative review' or uk_temp[6] == 'Exist other Offer':
            uk_list.append(uk_temp)
    if uk_list:
        for item in uk_list:
            print item
    else:
        print 'All Right'

    for i in range(de_Queue.qsize()):
        print de_Queue.get()
    for i in range(fr_Queue.qsize()):
        print fr_Queue.get()
    for i in range(es_Queue.qsize()):
        print es_Queue.get()
    for i in range(it_Queue.qsize()):
        print it_Queue.get()


multi_threading()