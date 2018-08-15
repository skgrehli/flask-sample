from jobwork.db_connection import db


class StateCollections(object):
    @classmethod
    def find(cls, *args, **kwargs):
        return db.statecollections.find(*args, **kwargs)

    @classmethod
    def find_one(cls, *args, **kwargs):
        return db.statecollections.find_one(*args, **kwargs)

    @classmethod
    def update(cls, *args, **kwargs):
        return db.statecollections.update(*args, **kwargs)

    @classmethod
    def insert(cls, *args, **kwargs):
        return db.statecollections.insert(*args, **kwargs)

    @classmethod
    def count(cls, *args, **kwargs):
        return db.statecollections.count(*args, **kwargs)
