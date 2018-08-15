from jobwork.db_connection import db


class UserPortfolio(object):
    @classmethod
    def find(cls, *args, **kwargs):
        return db.userportfolio.find(*args, **kwargs)

    @classmethod
    def find_one(cls, *args, **kwargs):
        return db.userportfolio.find_one(*args, **kwargs)

    @classmethod
    def update(cls, *args, **kwargs):
        return db.userportfolio.update(*args, **kwargs)

    @classmethod
    def insert(cls, *args, **kwargs):
        return db.userportfolio.insert(*args, **kwargs)

    @classmethod
    def count(cls, *args, **kwargs):
        return db.userportfolio.count(*args, **kwargs)
