#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from collections import defaultdict
from argparse import ArgumentParser
from urllib.request import urlopen
from bs4 import BeautifulSoup
from conf import *

def parsePage(page_url):

    page = urlopen(page_url)
    parsed_page = BeautifulSoup(page, 'lxml')

    return parsed_page

def printResults(stdscr ,results):
    for topic_name, topic_entries in results.iteritems():
        for index, entry in enumerate(topic_entries):
            stdscr.addstr(2, index + 5, str(index))
            stdscr.addstr(index + 3, 40, entry)
