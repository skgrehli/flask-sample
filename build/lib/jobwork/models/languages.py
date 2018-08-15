from jobwork.db_connection import db


class Languages(object):
    @classmethod
    def find(cls, *args, **kwargs):
        return db.languages.find(*args, **kwargs)

    @classmethod
    def find_one(cls, *args, **kwargs):
        return db.languages.find_one(*args, **kwargs)

    @classmethod
    def update(cls, *args, **kwargs):
        return db.languages.update(*args, **kwargs)

    @classmethod
    def insert(cls, *args, **kwargs):
        return db.languages.insert(*args, **kwargs)

    @classmethod
    def count(cls, *args, **kwargs):
        return db.languages.count(*args, **kwargs)
