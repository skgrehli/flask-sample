from jobwork.db_connection import db


class Categories(object):
    @classmethod
    def find(cls, *args, **kwargs):
        return db.categories.find(*args, **kwargs)

    @classmethod
    def find_one(cls, *args, **kwargs):
        return db.categories.find_one(*args, **kwargs)

    @classmethod
    def update(cls, *args, **kwargs):
        return db.categories.update(*args, **kwargs)

    @classmethod
    def insert(cls, *args, **kwargs):
        return db.categories.insert(*args, **kwargs)

    @classmethod
    def count(cls, *args, **kwargs):
        return db.categories.count(*args, **kwargs)
