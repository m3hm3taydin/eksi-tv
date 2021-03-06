#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from collections import defaultdict
from argparse import ArgumentParser
from urllib.request import urlopen
from bs4 import BeautifulSoup
from conf import *
#from common import *
#from entryHelper import *
import curses
from curses import wrapper
import time


def main(stdscr):
    k = 0
    cursor_x = 0
    cursor_y = 0

    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()



    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    
    #One time call crawler
    topic_results = get_popular_topics(POPULAR_PAGE_URL)

    cursor_y = 4
    cursor_x = 1
    # Loop where k is the last character pressed
    print_topics(topic_results, stdscr, cursor_y)

    while (k != ord('q')):

        # Initialization
        #stdscr.clear() #not needed i think
        height, width = stdscr.getmaxyx()

        if k == curses.KEY_DOWN:
            cursor_y = cursor_y + 1
            print_topics(topic_results, stdscr, cursor_y) #for color rendering
        elif k == curses.KEY_UP:
            cursor_y = cursor_y - 1
            print_topics(topic_results, stdscr, cursor_y) #for color rendering
        elif k == curses.KEY_RIGHT:
            cursor_x = cursor_x + 1
        elif k == curses.KEY_LEFT:
            cursor_x = cursor_x - 1

        cursor_x = max(0, cursor_x)
        cursor_x = min(width-1, cursor_x)

        cursor_y = max(0, cursor_y)
        cursor_y = min(height-1, cursor_y)

        # Declaration of strings
        title = "E-TV : Eksi Terminal Viewer"[:width-1]
        subtitle = "Written by Mehmet AYDIN"[:width-1]
        keystr = "Last key pressed: {}".format(k)[:width-1]
        menubarstr = "Eksi Sozluk Terminal Viewer"
        statusbarstr = "'q' to exit | 'r' to refresh | STATUS BAR | Pos: {}, {}".format(cursor_x, cursor_y)

        #below key gatchas

        if k == 0:
            keystr = "No key press detected..."[:width-1]
        if k == ord('r'):
            print_topics(topic_results, stdscr, cursor_y)
        if k == 10:
            entry_list = get_entries_for_selected_topic(topic_results, cursor_y - 5)
            selected_entry = 1

            padKey = 0
            entryPad = curses.newpad(height - 10, width - 90)
            
            cursor_pad_x = 0
            cursor_pad_y = 4

            while (padKey != ord('q')):
                # Create Entry Pad
                entryPad.clear()
                pad_height, pad_width = entryPad.getmaxyx()
                entryPad.addstr(1, 1 , str(padKey))

                if padKey == 66 or padKey == 258:
                    cursor_pad_y = cursor_pad_y + 1
                elif padKey == 65 or padKey == 259:
                    cursor_pad_y = cursor_pad_y - 1
                elif padKey == 67 or padKey == 260:
                    #right
                    #cursor_pad_x = cursor_pad_x + 1
                    current_page = selected_entry // 10
                    selected_entry = selected_entry + 1
                    
                    if selected_entry // 10 != current_page:
                        entry_list = get_entries_for_selected_topic(topic_results, cursor_y - 5, selected_entry // 10 + 1)


                elif padKey == 68 or padKey == 261:
                    #left
                    #cursor_pad_x = cursor_pad_x - 1
                    current_page = selected_entry // 10
                    if selected_entry > 1:
                        selected_entry = selected_entry - 1
                    
                    if selected_entry // 10 != current_page:
                        entry_list = get_entries_for_selected_topic(topic_results, cursor_y - 5, selected_entry // 10 + 1)

                cursor_pad_x = max(0, cursor_pad_x)
                cursor_pad_x = min(pad_width-1, cursor_pad_x)

                cursor_pad_y = max(0, cursor_pad_y)
                cursor_pad_y = min(pad_height-1, cursor_pad_y)

                #print topic name
                entryPad.attron(curses.A_BOLD)
                entryPad.attron(curses.color_pair(2))
                entryPad.addstr(4, 1 , "{0}\n\n".format(topic_results[cursor_y - 5][2]))
                entryPad.attroff(curses.A_BOLD)
                entryPad.attroff(curses.color_pair(2))

                entry = entry_list[selected_entry % 10]
                #print entry & author info
                entryPad.attron(curses.A_BOLD)
                entryPad.attron(curses.color_pair(2))
                entryPad.addstr("\n{0} -- {1}\n\n".format(entry.author, entry.entry_date))
                entryPad.attroff(curses.A_BOLD)
                entryPad.attroff(curses.color_pair(2))

                #print content
                entryPad.addstr(entry.content)

                #for printing all entries    
                # for index, entry in enumerate(entry_list):

                #     entryPad.attron(curses.A_BOLD)
                #     entryPad.attron(curses.color_pair(2))
                #     entryPad.addstr("\n{0} -- {1}\n".format(entry.author, entry.entry_date))
                #     entryPad.attroff(curses.A_BOLD)
                #     entryPad.attroff(curses.color_pair(2))

                #     entryPad.addstr("{0}".format(entry.content))

                  
                #entryPad.clrtobot()
                entryPad.move(cursor_pad_y, cursor_pad_x)
                entryPad.refresh(0, 0, 4, 80, height - 6, width - 10)

                padKey = entryPad.getch()
            
            #lets clear the screen & reload
            stdscr.clear()
            print_topics(topic_results, stdscr, cursor_y)

        






        #below is fixed data
        # Centering calculations

        start_x_title = int((width // 2) - (len(title) // 2) - len(title) % 2)
        start_x_subtitle = int((width // 2) - (len(subtitle) // 2) - len(subtitle) % 2)
        start_x_keystr = int((width // 2) - (len(keystr) // 2) - len(keystr) % 2)
        start_y = int((height // 2) - 2)

        # Render menu BAR
        stdscr.attron(curses.color_pair(3))
        stdscr.attron(curses.A_BOLD)
        stdscr.addstr(0, 0, menubarstr)
        whstr = "Width: {}, Height: {}".format(width, height)
        stdscr.addstr(0, len(menubarstr), " " * (width - len(menubarstr) - 1))
        stdscr.addstr(0, width - len(whstr), whstr)
        stdscr.attroff(curses.color_pair(3))


        # Render status bar
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(height-1, 0, statusbarstr)
        stdscr.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
        stdscr.attroff(curses.color_pair(3))

        # Turning on attributes for title
        stdscr.attron(curses.color_pair(2))
        stdscr.attron(curses.A_BOLD)
        stdscr.addstr(start_y, start_x_title, title)
        stdscr.attroff(curses.color_pair(2))
        stdscr.attroff(curses.A_BOLD)

        # Print rest of text
        stdscr.addstr(start_y + 1, start_x_subtitle, subtitle)
        stdscr.addstr(start_y + 3, (width // 2) - 2, '-' * 4)
        stdscr.addstr(start_y + 5, start_x_keystr, keystr)
        stdscr.move(cursor_y, cursor_x)


        # Refresh the screen
        #stdscr.refresh()

        # Wait for next input
        k = stdscr.getch()


# below will be moved to seperate files
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


def print_topics(topic_results, stdscr, cursor_y):
    for (t_index, t_link, t_name, t_entry_count) in topic_results:
        if (4 + t_index) == cursor_y:
            stdscr.attron(curses.color_pair(2))
            stdscr.attron(curses.A_BOLD)
            stdscr.addstr( 4 + t_index, 1, "{0} - {1} ({2})".format(t_index, t_name[0:41], str(t_entry_count)))
            stdscr.attroff(curses.color_pair(2))
            stdscr.attroff(curses.A_BOLD)
        else:
            stdscr.addstr( 4 + t_index, 1, "{0} - {1} ({2})".format(t_index, t_name[0:41], str(t_entry_count)))

def get_entries_for_selected_topic(results, selected_topic, page = 1):
    entries = []
    entries_page = parse_page(PAGE_URL+results[selected_topic][1]+'&p='+str(page))

    entry_list = entries_page.find_all('div','content')
    entry_info_list = entries_page.find_all('div', 'info')


    for index in range(len(entry_list)):
        content = entry_list[index].text
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


if __name__ == '__main__':
    wrapper(main)
