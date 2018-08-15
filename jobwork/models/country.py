from jobwork.db_connection import db


class CountryCollections(object):
    @classmethod
    def find(cls, *args, **kwargs):
        return db.country.find(*args, **kwargs)

    @classmethod
    def find_one(cls, *args, **kwargs):
        return db.country.find_one(*args, **kwargs)

    @classmethod
    def update(cls, *args, **kwargs):
        return db.country.update(*args, **kwargs)

    @classmethod
    def insert(cls, *args, **kwargs):
        return db.country.insert(*args, **kwargs)

    @classmethod
    def count(cls, *args, **kwargs):
        return db.countrycollections.count(*args, **kwargs)
