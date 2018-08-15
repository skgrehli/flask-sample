from jobwork.db_connection import db


class Report(object):
    @classmethod
    def find(cls, *args, **kwargs):
        return db.report.find(*args, **kwargs)

    @classmethod
    def find_one(cls, *args, **kwargs):
        return db.report.find_one(*args, **kwargs)

    @classmethod
    def update(cls, *args, **kwargs):
        return db.report.update(*args, **kwargs)

    @classmethod
    def insert(cls, *args, **kwargs):
        return db.report.insert(*args, **kwargs)

    @classmethod
    def count(cls, *args, **kwargs):
        return db.report.count(*args, **kwargs)
