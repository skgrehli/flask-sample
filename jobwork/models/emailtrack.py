from jobwork.db_connection import db


class EmailTracks(object):
    @classmethod
    def find(cls, *args, **kwargs):
        return db.emailtracks.find(*args, **kwargs)

    @classmethod
    def find_one(cls, *args, **kwargs):
        return db.emailtracks.find_one(*args, **kwargs)

    @classmethod
    def update(cls, *args, **kwargs):
        return db.emailtracks.update(*args, **kwargs)

    @classmethod
    def insert(cls, *args, **kwargs):
        return db.emailtracks.insert(*args, **kwargs)

    @classmethod
    def count(cls, *args, **kwargs):
        return db.emailtracks.count(*args, **kwargs)
