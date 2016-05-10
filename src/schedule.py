#!/usr/bin/python
# -*- coding: UTF-8 -*-

from send_mail import send_mail
from info_processor import info_process
from parse_data import parse_data, uk_Queue
import threading
import Queue
import time


def multi_threading():
    threading_list = []
    for country in ['de', 'uk', 'fr']:
        thread = threading.Thread(target=schedule, args=(country, ))
        thread.start()
        time.sleep(1)
    thread.join()


def schedule(country=None):
    info = info_process(country)
    for item in info:
        thread_name = 'thread_uk_%s' % item[1]
        thread_name = threading.Thread(target=parse_data, args=(item, ))
        thread_name.start()
        thread_name.join()
    for i in range(uk_Queue.qsize()):
        print uk_Queue.get()


multi_threading()
print 'Finished'

