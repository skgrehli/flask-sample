from jobwork.db_connection import db


class Invoice(object):
    @classmethod
    def find(cls, *args, **kwargs):
        return db.invoice.find(*args, **kwargs)

    @classmethod
    def find_one(cls, *args, **kwargs):
        return db.invoice.find_one(*args, **kwargs)

    @classmethod
    def update(cls, *args, **kwargs):
        return db.invoice.update(*args, **kwargs)

    @classmethod
    def insert(cls, *args, **kwargs):
        return db.invoice.insert(*args, **kwargs)

    @classmethod
    def count(cls, *args, **kwargs):
        return db.invoice.count(*args, **kwargs)
