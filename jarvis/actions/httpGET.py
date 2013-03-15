#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import re
from datetime import datetime
from BeautifulSoup import BeautifulSoup, SoupStrainer, BeautifulStoneSoup

'''
This class permits to get beers, epg, traffic and menu from websites :
    - http://www.lafinemousse.fr/carte
    - http://www.lafinemousse.fr/beers/search?locale=fr&query=kriek
    - http://tv.sfr.fr/epg/
    - http://www.transilien.com/trafic/detailtrafictravaux (HTTP)
    OR
    - http://www.transilien.com/flux/rss/traficLigne?codeLigne=B (RSS)
    - http://restauration-sfr.fr
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
            u'tf1': TF1_URL,
            u'france 2': FRANCE2_URL,
            u'france 3': FRANCE3_URL,
            u'france 5': FRANCE5_URL,
            u'm6': M6_URL,
            u'arté': ARTE_URL,
            u'd8': D8_URL,
            u'w9': W9_URL,
            u'france 4': FRANCE4_URL,
            u'bfm tv': BFM_URL,
            u'i télé': ITELE_URL,
            u'canalplus': CANALPLUS_URL,
            u'canalplus cinéma': CANALPLUSCINEMA_URL,
            u'canalplus sport': CANALPLUSSPORT_URL,
            u'canalplus family': CANALPLUSFAMILY_URL,
            u'fashion tv': FASHION_TV_URL,
            u'dorcel tv': DORCEL_URL,
            u'paris première': PARIS_PREMIERE_URL,
            u'téva': TEVA_URL,
            u'be in sport': BEINSPORT_URL,
            u'be in sport 2': BEINSPORT2_URL,
            u'girondins tv': GIRONDINS_TV_URL,
            u'm6 music black': M6_MUSIC_BLACK_URL,
            u'm6 music club': M6_MUSIC_CLUB_URL,
            u'm6 music hits': M6_MUSIC_HITS_URL,
            u'm6 boutique and co': M6_BOUTIQUE_AND_CO_URL,
            u'best of shopping': BEST_OF_SHOPPING_URL,
           }
##############################################################################

class httpGET():
    def __init__(self, website, _type='GET', data=None, cookies=None):
        if _type == 'GET':
            self.request = requests.get(website,
                                        data=data,
                                        cookies=cookies)
        elif _type == 'POST':
            self.request = requests.post(website,
                                         data=data,
                                         cookies=cookies)

        # Definep page
        self._page = self.request.text

    def return_beers(self):
        beers_links = SoupStrainer('a', href=re.compile('beers'))
        soup = BeautifulSoup(self._page, parseOnlyThese=beers_links)
        beers = []
        intro = u"Voici les nouvelles bières à la fine mousse :"
        beers.append(intro)
        for tag in soup.findAll("a"):
            beers.append(tag.string.split('(')[0].strip())
        return beers

    def return_menu(self):
        # Grep html page
        soup = BeautifulSoup(self._page, convertEntities=BeautifulSoup.HTML_ENTITIES)

        # Define output variable
        menu = {}

        # Extract menu
        for tag in soup.findAll("div", attrs='menu-body'):
            for subtag in tag.findAll("span"):
                if '=' in subtag.text:
                    continue
                elif subtag.text == u'Plats du jour':
                    key = subtag.text
                    menu[key] = []
                elif subtag.text == u'Légumes du jour':
                    key = subtag.text
                    menu[key] = []
                else:
                    menu[key].append(subtag.text)
        return menu

    def return_epg(self, stream, full=False):
        # Init variables
        today = datetime.now()

        # Grep html page
        soup = BeautifulSoup(self._page)

        # Define containers to extract data
        main_container = {'class': 'epg_element_prog_container'}
        sub_attrs = {
                        'deb_prog hidden': 'heure début',
                        'fin_prog hidden': 'heure fin',
                        'lib_prog': 'titre',
                        'duree_prog hidden' : 'durée',
                        'duree_prog': 'durée',
                        'desc_prog': 'description',
                        'img_prog': 'photo',
                    }

        # Extract data from containers
        full_epg = list()
        for tag in soup.findAll("div", attrs=main_container):
            epg = dict()
            for div in tag.findAll("div"):
                if div["class"] in sub_attrs:
                    if div["class"] == 'img_prog':
                        epg[sub_attrs[div["class"]]] = str(div.find('img')['alt'])
                    else:
                        epg[sub_attrs[div["class"]]] = str(div.string)
            if epg != {}:
                # Define stream name
                epg ['chaine'] = stream

                # Define photo
                if 'photo' in epg and epg['photo'] != '':
                    epg['photo'] = 'http://static-tv.s-sfr.fr/img/epg/' + epg['photo']
                else:
                    epg['photo'] = None

                # Init description if not defined
                if 'description' not in epg:
                    epg['description'] = None

                if full:
                    # Add epg in full list
                    full_epg.append(epg)
                else:
                    if datetime.fromtimestamp(int(epg['heure début'])) <= today \
                       and \
                       datetime.fromtimestamp(int(epg['heure fin'])) >= today:
                        # Add epg in full list
                        full_epg.append(epg)
                        break
        return full_epg


    def return_traffic(self):
        # Grep html page
        soup = BeautifulSoup(self._page, fromEncoding="utf-8")

        # Define container to extract data
        container = {'class': 'etat_trafic_bloc'}

        # Init output variable
        traffic = ''
        signature = 'SNCF Transilien'
        for tag in soup.findAll("div", attrs=container):
            for div in tag.findAll("h2"):
                traffic += div.text + '\n'
            for div in tag.findAll("p"):
                traffic += div.text + '\n'
        traffic = traffic[:traffic.find(signature)].strip()
        traffic = BeautifulStoneSoup(traffic, convertEntities=BeautifulStoneSoup.HTML_ENTITIES)
        return unicode(traffic)

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
        print ','.join(get.return_beers())
    elif action == 'menu':
        # First step to get cookie
        website = 'http://restauration-sfr.fr/Restaurant.aspx?spsId=249'
        # Init httpGET object with given website
        get = httpGET(website)

        # Last step to get menu
        website = 'http://restauration-sfr.fr/ajaxWidgetMenu.aspx'
        # Init sample data to post
        data = 'divId=8131&spsId=249&day=2013-03-14&widgetMenu=false'
        # Init httpGET object with given website, data and cookie
        get = httpGET(website,
                      _type='POST',
                      data=data,
                      cookies=get.request.cookies)
        print get.return_menu()
    elif action == 'traffic':
        website = 'http://www.transilien.com/trafic/detailtrafictravaux/init?categorie=trafic&codeLigne=A'
        # Init httpGET object with given website
        get = httpGET(website)
        print get.return_traffic()
    elif action == 'epg':
        if len(input_string) != 0:
            stream = ' '.join(input_string)
            if stream in EPG_URLS:
                website = EPG_URLS[stream]

                # Init httpGET object with given website
                get = httpGET(website)
                print get.return_epg(stream)
            else:
                print "Your stream is not defined in : %s" % EPG_URLS.keys()
                sys.exit(1)
        else:
            for stream in EPG_URLS:
                print stream
                website = EPG_URLS[stream]

                # Init httpGET object with given website
                get = httpGET(website)
                print get.return_epg(stream)
    else:
        print 'Given action is not defined!\nOnly beer or epg for now'
        sys.exit(1)

    sys.exit(0)
