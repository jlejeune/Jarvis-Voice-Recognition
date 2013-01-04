#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2
import re
from datetime import datetime
from BeautifulSoup import BeautifulSoup, SoupStrainer

'''
This class permits to get beers and epg from websites :
    - http://www.lafinemousse.fr/carte
    - http://www.lafinemousse.fr/beers/search?locale=fr&query=kriek
    - http://tv.sfr.fr/epg/

'''

##############################################################################
# EPG URLS
PREFIX_URL = 'http://tv.sfr.fr/epg/maintenant/'
# Classic
TF1_URL = PREFIX_URL + '?id_chaine=1'
FRANCE2_URL = PREFIX_URL + '?id_chaine=2'
FRANCE3_URL = PREFIX_URL + '?id_chaine=3'
CANALPLUS_URL = PREFIX_URL + '?id_chaine=4'
FRANCE5_URL = PREFIX_URL + '?id_chaine=5'
M6_URL = PREFIX_URL + '?id_chaine=6'
ARTE_URL = PREFIX_URL + '?id_chaine=7'
D8_URL = PREFIX_URL + '?id_chaine=8'
W9_URL = PREFIX_URL + '?id_chaine=9'
FRANCE4_URL = PREFIX_URL + '?id_chaine=14'
BFM_URL = PREFIX_URL + '?id_chaine=15'
ITELE_URL = PREFIX_URL + '?id_chaine=16'
TEVA_URL = PREFIX_URL + '?id_chaine=27'
PARIS_PREMIERE_URL = PREFIX_URL + '?id_chaine=27'
FASHION_TV_URL = PREFIX_URL + '?id_chaine=116'
# CANAL +
CANALPLUSCINEMA_URL = PREFIX_URL + 'Les%20chaînes%20Canal%20+-4/?id_chaine=23'
CANALPLUSSPORT_URL = PREFIX_URL + 'Les%20chaînes%20Canal%20+-4/?id_chaine=24'
CANALPLUSFAMILY_URL = PREFIX_URL + 'Les%20chaînes%20Canal%20+-4/?id_chaine=25'
# DORCEL
DORCEL_URL = PREFIX_URL + 'Grand%20Spectacle-9/?id_chaine=128'
# BE IN SPORT
BEINSPORT_URL = PREFIX_URL + 'Sélection%20+%20beIN%20SPORT-11/?id_chaine=20'
BEINSPORT2_URL = PREFIX_URL + 'Sélection%20+%20beIN%20SPORT-11/?id_chaine=21'
GIRONDINS_TV_URL = PREFIX_URL + 'Sélection%20+%20beIN%20SPORT-11/?id_chaine=57'
# M6
M6_MUSIC_BLACK_URL = PREFIX_URL + 'Sélection%20+%20beIN%20SPORT-11/?id_chaine=96'
M6_MUSIC_CLUB_URL = PREFIX_URL + 'Sélection%20+%20beIN%20SPORT-11/?id_chaine=97'
M6_MUSIC_HITS_URL = PREFIX_URL + '?id_chaine=86'
M6_BOUTIQUE_AND_CO_URL = PREFIX_URL + '?id_chaine=71'
# Others
BEST_OF_SHOPPING_URL = PREFIX_URL + '?id_chaine=73'

EPG_URLS = {
            'tf1': TF1_URL,
            'france 2': FRANCE2_URL,
            'france 3': FRANCE3_URL,
            'france 5': FRANCE5_URL,
            'm6': M6_URL,
            'arté': ARTE_URL,
            'd8': D8_URL,
            'w9': W9_URL,
            'france 4': FRANCE4_URL,
            'bfm tv': BFM_URL,
            'i télé': ITELE_URL,
            'canalplus': CANALPLUS_URL,
            'canalplus cinéma': CANALPLUSCINEMA_URL,
            'canalplus sport': CANALPLUSSPORT_URL,
            'canalplus family': CANALPLUSFAMILY_URL,
            'fashion tv': FASHION_TV_URL,
            'dorcel tv': DORCEL_URL,
            'paris première': PARIS_PREMIERE_URL,
            'téva': TEVA_URL,
            'be in sport': BEINSPORT_URL,
            'be in sport 2': BEINSPORT2_URL,
            'girondins tv': GIRONDINS_TV_URL,
            'm6 music black': M6_MUSIC_BLACK_URL,
            'm6 music club': M6_MUSIC_CLUB_URL,
            'm6 music hits': M6_MUSIC_HITS_URL,
            'm6 boutique and co': M6_BOUTIQUE_AND_CO_URL,
            'best of shopping': BEST_OF_SHOPPING_URL,
           }
##############################################################################

class httpGET():
    def __init__(self, website):
        self.website = website
        self._page = urllib2.urlopen(self.website)

    def return_menu(self):
        beers_links = SoupStrainer('a', href=re.compile('beers'))
        soup = BeautifulSoup(self._page, parseOnlyThese=beers_links)
        beers = []
        intro = u"Voici les nouvelles bières à la fine mousse :"
        beers.append(intro)
        for tag in soup.findAll("a"):
            beers.append(tag.string.split('(')[0].strip())
        return beers

    def return_epg(self):
        # Init variables
        today = datetime.now()
        time = today.time()

        # Grep html page
        soup = BeautifulSoup(self._page)

        # Define containers to extract data
        main_container = {'class': 'epg_element_prog_container'}
        sub_attrs = {
                        'date_prog hidden': 'jour',
                        'heure_prog': 'heure début',
                        'heurefin_prog hidden': 'heure fin',
                        'lib_prog': 'titre',
                        'duree_prog hidden' : 'durée',
                        'duree_prog': 'durée',
                        'desc_prog': 'description',
                        'img_prog': 'photo',
                    }

        # Extract data from containers
        for tag in soup.findAll("div", attrs=main_container):
            epg = dict()
            for div in tag.findAll("div"):
                if div["class"] in sub_attrs:
                    if div["class"] == 'img_prog':
                        epg[sub_attrs[div["class"]]] = str(div.find('img')['alt'])
                    else:
                        epg[sub_attrs[div["class"]]] = str(div.string)
            if epg != {}:
                if datetime.strptime(epg['heure début'], '%H:%M').time() <= time \
                   and \
                   datetime.strptime(epg['heure fin'], '%H:%M').time() >= time:
                    if epg['photo'] != '':
                        epg['photo'] = 'http://static-tv.s-sfr.fr/img/epg/' + epg['photo']
                    else:
                        epg['photo'] = None
                    break
        return epg

if __name__ == "__main__":
    import sys
    input_string = sys.argv

    if len(input_string) < 2:
        print("Usage: python %s action [arg]." % input_string[0])
        sys.exit(1)

    # Remove the program name from the argv list
    input_string.pop(0)
    # Analyze given action which should be now the first arg
    action = input_string.pop(0)
    if action == 'beer':
        website = 'http://www.lafinemousse.fr/carte'
        # Init httpGET object with given website
        get = httpGET(website)
        print ','.join(get.return_menu())
    elif action == 'epg':
        if len(input_string) != 0:
            stream = input_string.pop(0)
            if stream in EPG_URLS:
                website = EPG_URLS[stream]
            else:
                print "Your stream is not defined in : %s" % EPG_URLS.keys()
                sys.exit(1)
        else:
            print "You have to specify a stream arg in : %s" % EPG_URLS.keys()
            sys.exit(1)

        # Init httpGET object with given website
        get = httpGET(website)
        print get.return_epg()
    else:
        print 'Given action is not defined!\nOnly beer or epg for now'
        sys.exit(1)

    sys.exit(0)
