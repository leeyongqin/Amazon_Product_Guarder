#!/usr/bin/python
# -*- coding: UTF-8 -*-

from send_mail import send_mail
from info_processor import info_process
from parse_data import parse_data, uk_Queue
import threading
import Queue
import time

info_uk = info_process('uk')
threading_list = []
for item in info_uk:
    thread_name = 'thread_uk_%s' % item[1]
    thread_name = threading.Thread(target=parse_data, args=(item, ))
    thread_name.start()
    thread_name.join()
for i in range(uk_Queue.qsize()):
    print uk_Queue.get()

print 'Finished'

