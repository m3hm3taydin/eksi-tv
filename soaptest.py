#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from collections import defaultdict
from argparse import ArgumentParser
from urllib.request import urlopen
from bs4 import BeautifulSoup
import os
import curses
from conf import *


PAGE_URL = 'https://eksisozluk.com'

def main():
 
    topic_results = get_popular_topics(POPULAR_PAGE_URL)

    #found topics
    #print(topic_results)

    #get entries for selected topic
    get_entries_for_selected_topic(topic_results, 1)

def parse_page(page_url):

    page = urlopen(page_url)
    parsed_page = BeautifulSoup(page, 'lxml')

    return parsed_page

def get_popular_topics(page_url):
    results = []
    topic_list = parse_page(page_url).find('ul', 'topic-list partial')

    links = topic_list('a')

    for index, link in enumerate(links):
        topic_link = link['href']
        topic_name = link.contents[0]

        if "," in link.contents[1].string:
            splitted_count = link.contents[1].string.split(",")
            number_of_entries_for_topic = int(splitted_count[0]) * 1000 + int(splitted_count[1][0]) * 100
        else:
            number_of_entries_for_topic = int(link.contents[1].string)

        results.append((index+1, topic_link, topic_name, number_of_entries_for_topic))

    return results

def get_entries_for_selected_topic(results, selected_topic):
    entries = []
    entries_page = parse_page(PAGE_URL+results[selected_topic][1])

    entry_list = entries_page.find_all('div','content')
    entry_info_list = entries_page.find_all('div', 'info')


    for index in range(len(entry_list)):
        content = entry_list[index].text
        print(content)
        permalink = entry_info_list[index].find_all('a', 'entry-date permalink', href = True)[0]['href']
        entry_date = entry_info_list[index].find_all('a', 'entry-date permalink', href = True)[0].text
        author = entry_info_list[index].find_all('a', 'entry-author', href = True)[0].text

        entry = Entry(content, permalink, entry_date, author)
        entries.append(entry)

    return entries

class Entry():
    def __init__(self, content, permalink, entry_date, author):
        self.content = content
        self.permalink = permalink
        self.entry_date = entry_date
        self.author = author

if __name__ == "__main__":
    main()
