#!/usr/bin/python
# -*- coding: UTF-8 -*-

from send_mail import send_mail
from info_processor import info_process
from parse_data import parse_data

info = info_process('us')
for item in info:
    parse_data(item)