# -*- coding: utf-8 -*-
# vim:set ai et sts=4 sw=4:

import logging
import re
from datetime import datetime
from flask import Response, Blueprint, json

from jarvis.actions.httpGET import httpGET


menu = Blueprint('menu', __name__)

logger = logging.getLogger('jarvis-server.menu')


### GET methods ###
@menu.route('/menu', methods=['GET'])
@menu.route('/menu/<date>', methods=['GET'])
def get_menu(date=None):
    """
    Return menu
    @param date : string (%Y)
    """
    # First step to get cookie
    website = 'http://restauration-sfr.fr/Restaurant.aspx?spsId=249'
    get = httpGET(website)

    # Last step to get menu
    website = 'http://restauration-sfr.fr/ajaxWidgetMenu.aspx'

    # Check date
    if date!= None and not re.compile(r'(\d){8}').search(date):
        return 'Given date \'%s\' is not in the good shape, it must be YYYYMMDD' % date, 500

    if date == None:
        date = datetime.now()
        date = date.strftime('%Y-%m-%d')
    else:
        date = datetime.strptime(date, '%Y%m%d').strftime('%Y-%m-%d')

    # Init sample data to post
    data = 'divId=8131&spsId=249&day=%s&widgetMenu=false' % date

    # Init httpGET object with given website, data and cookie
    get = httpGET(website,
                  _type='POST',
                  data=data,
                  cookies=get.request.cookies)

    # Make json ouput
    menu = {date: get.return_menu()}

    return Response(json.dumps(menu, ensure_ascii=False),
                    content_type='application/json; charset=utf-8')
