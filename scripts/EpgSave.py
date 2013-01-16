#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime
from sqlite3 import IntegrityError
from jarvis.flask.models.epg import Epg
from jarvis.actions.httpGET import httpGET, EPG_URLS

if __name__ == "__main__":
    for stream in EPG_URLS:
        # Get matching website
        website = EPG_URLS[stream]

        # Init httpGET object with given website
        try:
            get = httpGET(website)
        except Exception, err:
            print 'Error \'%s\' with this wbesite \'%s\'' % (err, website)
            continue
        epg = get.return_epg(stream, full=True)

        # Save prog in epg database
        for prog in epg:
            try:
                Epg.create(
                    start=datetime.fromtimestamp(int(prog['heure début'])),
                    end=datetime.fromtimestamp(int(prog['heure fin'])),
                    stream=prog['chaine'],
                    title=prog['titre'],
                    description=prog['description'],
                    photo=prog['photo'],
                    duration=prog['durée'],
                )
            except IntegrityError, err:
                pass
            except Exception, err:
                print 'Error in save %s for stream %s : %s' % (prog,
                                                               stream,
                                                               err)
