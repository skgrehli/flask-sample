from jobwork.db_connection import db


class Skills(object):
    @classmethod
    def find(cls, *args, **kwargs):
        return db.skills.find(*args, **kwargs)

    @classmethod
    def find_one(cls, *args, **kwargs):
        return db.skills.find_one(*args, **kwargs)

    @classmethod
    def update(cls, *args, **kwargs):
        return db.skills.update(*args, **kwargs)

    @classmethod
    def insert(cls, *args, **kwargs):
        return db.skills.insert(*args, **kwargs)

    @classmethod
    def count(cls, *args, **kwargs):
        return db.skills.count(*args, **kwargs)
