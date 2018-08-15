from jobwork.db_connection import db


class Conversations(object):
    @classmethod
    def find(cls, *args, **kwargs):
        return db.conversations.find(*args, **kwargs)

    @classmethod
    def find_one(cls, *args, **kwargs):
        return db.conversations.find_one(*args, **kwargs)

    @classmethod
    def update(cls, *args, **kwargs):
        return db.conversations.update(*args, **kwargs)

    @classmethod
    def insert(cls, *args, **kwargs):
        return db.conversations.insert(*args, **kwargs)

    @classmethod
    def count(cls, *args, **kwargs):
        return db.conversations.count(*args, **kwargs)
