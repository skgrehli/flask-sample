from jobwork.db_connection import db


class Messages(object):
    @classmethod
    def find(cls, *args, **kwargs):
        return db.messages.find(*args, **kwargs)

    @classmethod
    def find_one(cls, *args, **kwargs):
        return db.messages.find_one(*args, **kwargs)

    @classmethod
    def update(cls, *args, **kwargs):
        return db.messages.update(*args, **kwargs)

    @classmethod
    def insert(cls, *args, **kwargs):
        return db.messages.insert(*args, **kwargs)

    @classmethod
    def count(cls, *args, **kwargs):
        return db.messages.count(*args, **kwargs)
