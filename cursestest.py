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

def main():
    topic_results = getTopics(POPULAR_PAGE_URL)
    print("topic_result alındı")
    requested_topic_entries = getEntriesForSelectedTopic(topic_results, 2)
    print("2 numaralı topic entries alındı")
    #stdscr.addstr(1, 40, str(selectMatch))
    for topic_name, topic_entries in requested_topic_entries.items():
        print(topic_name)
        for index, entry in enumerate(topic_entries):
            print("{0} - ({1})".format(index, entry))


def getEntriesForTopic(topic_link, entry_count_per_topic):

    topic_page_content = parsePage(PAGE_URL +  topic_link.decode('utf-8'))
    entry_list_container = topic_page_content.find('ul', {'id': 'entry-list'})
    print(entry_list_container)
    #entries_for_topic = entry_list_container.findAll('div', 'content')[:entry_count_per_topic]

    return [entry.text for entry in entries_for_topic]


def getEntriesForSelectedTopic(results, topic_index):

    #selected_topic_links = []
    selected_topic_entries = defaultdict(list)

    for topic_result in results:
        if topic_index == topic_result[0]:
            topic_link = topic_result[1]
            topic_name = topic_result[2]

            #selected_topic_links.append(topic_link)
            selected_topic_entries[topic_name] = getEntriesForTopic(topic_link, 10)

    return selected_topic_entries

def parsePage(page_url):

    page = urlopen(page_url)
    parsed_page = BeautifulSoup(page, 'lxml')

    return parsed_page



def getTopics(url):

    results = []
    parsed_page = parsePage(url)
    topic_list = parsed_page.find('ul', 'topic-list partial')

    links = topic_list('a')

    for index, link in enumerate(links):
        topic_link = link['href'].encode('utf-8')
        topic_name = link.contents[0].encode('utf-8')

        if "," in link.contents[1].string:
            splitted_count = link.contents[1].string.split(",")
            number_of_entries_for_topic = int(splitted_count[0]) * 1000 + int(splitted_count[1][0]) * 100
        else:
            number_of_entries_for_topic = int(link.contents[1].string)

        results.append((index+1, topic_link, topic_name, number_of_entries_for_topic))

    return results



if __name__ == "__main__":
    main()
