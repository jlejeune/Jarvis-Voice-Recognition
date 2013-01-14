# -*- coding: utf-8 -*-
# vim:set ai et sts=4 sw=4:

import peewee
from datetime import datetime

db = peewee.SqliteDatabase('/var/lib/jarvis-server/epg.db')

class Epg(peewee.Model):
    start = peewee.DateTimeField()
    end = peewee.DateTimeField()
    stream = peewee.CharField()
    title = peewee.CharField()
    description = peewee.CharField(null=True)
    photo = peewee.CharField(null=True)
    duration = peewee.CharField()

    class Meta:
        database = db
        # Define indexes
        indexes = (
            (('start', 'end', 'stream'), True),
        )

    def to_json(self):
        return {
                'title'       : self.title,
                'start'       : self.start.strftime('%Y-%m-%d %H:%M:%S'),
                'end'         : self.end.strftime('%Y-%m-%d %H:%M:%S'),
                'stream'      : self.stream,
                'description' : self.description,
                'photo'       : self.photo,
                'duration'    : self.duration
               }

    def get_epg(self, stream, full=False):
        try:
            if full:
                epg = Epg.select().where(Epg.stream == stream)
            else:
                epg = Epg.select().where((Epg.stream == stream) \
                                         & \
                                         (Epg.start <= datetime.now()) \
                                         & \
                                         (Epg.end >= datetime.now()) \
                                         )
            return epg
        except Exception, err:
            return err

    def get_full_epg(self, full=False):
        try:
            if full:
                epg = Epg.select()
            else:
                epg = Epg.select().where((Epg.start <= datetime.now()) \
                                         & \
                                         (Epg.end >= datetime.now()) \
                                         )
            return epg
        except Exception, err:
            return err
