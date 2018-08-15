from jobwork.db_connection import db


class StripeCustomers(object):
    @classmethod
    def find(cls, *args, **kwargs):
        return db.stripecustomers.find(*args, **kwargs)

    @classmethod
    def find_one(cls, *args, **kwargs):
        return db.stripecustomers.find_one(*args, **kwargs)

    @classmethod
    def update(cls, *args, **kwargs):
        return db.stripecustomers.update(*args, **kwargs)

    @classmethod
    def insert(cls, *args, **kwargs):
        return db.stripecustomers.insert(*args, **kwargs)

    @classmethod
    def count(cls, *args, **kwargs):
        return db.stripecustomers.count(*args, **kwargs)
