from jobwork.db_connection import db


class Jobs(object):
    @classmethod
    def find(cls, *args, **kwargs):
        return db.jobs.find(*args, **kwargs)

    @classmethod
    def find_one(cls, *args, **kwargs):
        return db.jobs.find_one(*args, **kwargs)

    @classmethod
    def update(cls, *args, **kwargs):
        return db.jobs.update(*args, **kwargs)

    @classmethod
    def insert(cls, *args, **kwargs):
        return db.jobs.insert(*args, **kwargs)

    @classmethod
    def count(cls, *args, **kwargs):
        return db.jobs.count(*args, **kwargs)
