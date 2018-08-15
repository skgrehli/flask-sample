from jobwork.db_connection import db


class JobBids(object):
    @classmethod
    def find(cls, *args, **kwargs):
        return db.jobbids.find(*args, **kwargs)

    @classmethod
    def find_one(cls, *args, **kwargs):
        return db.jobbids.find_one(*args, **kwargs)

    @classmethod
    def update(cls, *args, **kwargs):
        return db.jobbids.update(*args, **kwargs)

    @classmethod
    def insert(cls, *args, **kwargs):
        return db.jobbids.insert(*args, **kwargs)

    @classmethod
    def count(cls, *args, **kwargs):
        return db.jobbids.count(*args, **kwargs)
