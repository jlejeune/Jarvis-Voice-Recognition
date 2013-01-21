# -*- coding: utf-8 -*-
# vim:set ai et sts=4 sw=4:

import logging
from flask import Blueprint, json, Response
from jarvis.actions.rssRead import Feed

traffic = Blueprint('traffic', __name__)

logger = logging.getLogger('jarvis-server.traffic')


### GET methods ###
@traffic.route('/traffic/<train>', methods=['GET'])
def get_traffic(train):
    """
    Get traffic for given train (between : A, B, C, D, E, H, J, K, L, N, P, R, U)
    @param train : letter 
    """
    valid_trains = ('A', 'B', 'C', 'D', 'E', 'H', 'J', 'K', 'L', 'N', 'P', 'R', 'U')
    if train in valid_trains:
        root_website = 'http://www.transilien.com/flux/rss/traficLigne?codeLigne='
        website = root_website + train
        # Init Feed object with given website
        feed = Feed(website)
        dict_traffic = {train: feed.body()}
        return Response(json.dumps(dict_traffic, ensure_ascii=False),
                        content_type='application/json; charset=utf-8')
    else:
        return 'Your train must be in [%s]' % ', '.join(valid_trains), 500
