from jobwork.db_connection import db


class Locations(object):
    @classmethod
    def find(cls, *args, **kwargs):
        return db.location.find(*args, **kwargs)

    @classmethod
    def find_one(cls, *args, **kwargs):
        return db.location.find_one(*args, **kwargs)

    @classmethod
    def update(cls, *args, **kwargs):
        return db.location.update(*args, **kwargs)

    @classmethod
    def insert(cls, *args, **kwargs):
        return db.location.insert(*args, **kwargs)

    @classmethod
    def count(cls, *args, **kwargs):
        return db.location.count(*args, **kwargs)

    @classmethod
    def aggregate(cls, *args, **kwargs):
        return db.location.aggregate(*args, **kwargs)
