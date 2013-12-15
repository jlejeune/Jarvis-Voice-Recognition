# -*- coding: utf-8 -*-
# vim:set ai et sts=4 sw=4:

import logging
from flask import Blueprint, json, Response
from jarvis.actions.rssRead import Feed

traffic = Blueprint('traffic', __name__)

logger = logging.getLogger('jarvis-server.traffic')

VALID_TRAINS = ('A', 'B', 'C', 'D', 'H', 'J', 'L', 'N', 'P')


### GET methods ###
@traffic.route('/traffic/<train>', methods=['GET'])
@traffic.route('/traffic', methods=['GET'])
def get_traffic(train=None):
    """
    Get traffic for given train (between : A, B, C, D, H, J, L, N, P)
    @param train : letter
    """
    if train is not None and train not in VALID_TRAINS:
        return 'Your train must be in [%s]' % ', '.join(VALID_TRAINS), 400

    if train is None:
        website = 'http://www.transilien.com/flux/rss/traficLigne'
        # Init Feed object with given website and get body
        body = Feed(website).body()
        dict_traffic = {}
        for event in body:
            # Hack to malformed lines
            if len(event['title'].split(':')) != 2:
                continue

            # Define tab by train
            train = event['title'].split(':')[0].strip()
            if train not in dict_traffic:
                dict_traffic[train] = []

            # Clean event before appending it to train tab
            event['status'] = event['title'].split(':')[1].strip()
            del event['title']
            dict_traffic[train].append(event)
    else:
        root_website = 'http://www.transilien.com/flux/rss/traficLigne?codeLigne='
        website = root_website + train
        # Init Feed object with given website and get body
        body = Feed(website).body()
        for event in body:
            event['status'] = event['title'].split(':')[1].strip()
            del event['title']
        dict_traffic = {train: body}

    return Response(json.dumps(dict_traffic, ensure_ascii=False),
                    content_type='application/json; charset=utf-8')
