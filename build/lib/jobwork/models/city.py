from jobwork.db_connection import db


class CityCollections(object):
    @classmethod
    def find(cls, *args, **kwargs):
        return db.city.find(*args, **kwargs)

    @classmethod
    def find_one(cls, *args, **kwargs):
        return db.city.find_one(*args, **kwargs)

    @classmethod
    def update(cls, *args, **kwargs):
        return db.city.update(*args, **kwargs)

    @classmethod
    def insert(cls, *args, **kwargs):
        return db.city.insert(*args, **kwargs)

    @classmethod
    def count(cls, *args, **kwargs):
        return db.city.count(*args, **kwargs)
