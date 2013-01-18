# -*- coding: utf-8 -*-
# vim:set ai et sts=4 sw=4:

import logging
from flask import Blueprint, json, Response
from jarvis.actions.httpGET import httpGET

traffic = Blueprint('traffic', __name__)

logger = logging.getLogger('jarvis-server.traffic')


### GET methods ###
@traffic.route('/traffic/<train>', methods=['GET'])
def get_traffic(train):
    """
    Get traffic for given train (between : A, B, C, D, E ?)
    @param train : letter 
    """
    valid_trains = ('A', 'B', 'C', 'D', 'E', 'H', 'J', 'K', 'L', 'N', 'P', 'R', 'U')
    if train in valid_trains:
        root_website = 'http://www.transilien.com/trafic/detailtrafictravaux/init?categorie=trafic&codeLigne='
        website = root_website + train
        # Init httpGET object with given website
        get = httpGET(website)
        dict_traffic = {train: get.return_traffic()}
        return Response(json.dumps(dict_traffic, ensure_ascii=False),
                        content_type='application/json; charset=utf-8')
    else:
        return 'Your train must be in [%s]' % ', '.join(valid_trains), 500
