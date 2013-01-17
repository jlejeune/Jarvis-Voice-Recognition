# -*- coding: utf-8 -*-
# vim:set ai et sts=4 sw=4:

import peewee
from datetime import datetime
from jarvis.flask import options

sqlite_database = options.basedir + 'epg.db'
db = peewee.SqliteDatabase(sqlite_database)

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

if __name__ == "__main__":
    '''
    Unit test to valid Epg model class
    '''
    import sys
    from sqlite3 import OperationalError

    # Save given arg and test it
    input_string = sys.argv
    if len(input_string) < 2:
        print("Usage: python %s action [arg]." % input_string[0])
        sys.exit(1)

    # Remove the program name from the argv list
    input_string.pop(0)

    # Analyze given action which should be now the first arg
    action = input_string.pop(0)

    if action == 'init':
        try:
            # Init table
            Epg.create_table()
        except OperationalError, err:
            print err
            sys.exit(1)
    elif action == 'test':
        try:
            # Create sample epg
            Epg.create(
                start = datetime.now().replace(microsecond=0),
                end = datetime.now().replace(microsecond=0),
                stream = "tf1",
                title = "Journal",
                description = "test",
                photo = None,
                duration = "35min",
            )
        except OperationalError, err:
            print err
            sys.exit(1)
    elif action == 'cleantest':
        # Select * from epg where description == test
        delete_query = Epg.delete().where(Epg.description == 'test')
        try:
            delete_query.execute()
        except OperationalError, err:
            print err
            sys.exit(1)
    elif action == 'clean':
        # Select * from epg where start < today (at midnight)
        midnight = datetime.now().replace(hour=0, minute=0, second=0,
                microsecond=0)
        delete_query = Epg.delete().where(Epg.start <= midnight)
        try:
            delete_query.execute()
        except OperationalError, err:
            print err
            sys.exit(1)
    elif action == 'select':
        if len(input_string) != 0:
            stream = input_string.pop(0)
            # Select prog from epg for given stream currently
            epg = Epg.select().where((Epg.stream == stream) \
                                     & \
                                     (Epg.start <= datetime.now()) \
                                     & \
                                     (Epg.end >= datetime.now()) \
                                    )
            try:
                for prog in epg:
                    print prog.stream, prog.title, prog.start, prog.end
            except OperationalError, err:
                print err
                sys.exit(1)
        else:
            # Select * from epg
            epg = Epg.select()
            try:
                for prog in epg:
                    print prog.stream, prog.title, prog.start, prog.end
            except OperationalError, err:
                print err
                sys.exit(1)
    sys.exit(0)
