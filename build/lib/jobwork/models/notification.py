from jobwork.db_connection import db


class Notifications(object):
    @classmethod
    def find(cls, *args, **kwargs):
        return db.notification.find(*args, **kwargs)

    @classmethod
    def find_one(cls, *args, **kwargs):
        return db.notification.find_one(*args, **kwargs)

    @classmethod
    def update(cls, *args, **kwargs):
        return db.notification.update(*args, **kwargs)

    @classmethod
    def insert(cls, *args, **kwargs):
        return db.notification.insert(*args, **kwargs)

    @classmethod
    def count(cls, *args, **kwargs):
        return db.notification.count(*args, **kwargs)
