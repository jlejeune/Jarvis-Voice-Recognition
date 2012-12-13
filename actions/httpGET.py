#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2
import re
from BeautifulSoup import BeautifulSoup, SoupStrainer

'''
This class permits to get content from HTML websites :
    - http://www.lafinemousse.fr/carte
    - http://www.lafinemousse.fr/beers/search?locale=fr&query=kriek

'''


class httpGET():
    def __init__(self, website):
        self.website = website
        self._page = urllib2.urlopen(self.website)

    def return_menu(self):
        beers_links = SoupStrainer('a', href=re.compile('beers'))
        soup = BeautifulSoup(self._page, parseOnlyThese=beers_links)
        beers = []
        for tag in soup.findAll("a"):
            beers.append(tag.string.split('(')[0].strip())
        return beers

if __name__ == "__main__":
    import sys
    input_string = sys.argv

    if len(input_string) < 2:
        print("Usage: python %s website_url."
                % input_string[0])
        sys.exit(1)

    # Remove the program name from the argv list
    input_string.pop(0)
    # Take the language which should be now the first args
    website = input_string[0]

    # Init httpGET object with given website
    get = httpGET(website)
    print ','.join(get.return_menu())

    sys.exit(0)
