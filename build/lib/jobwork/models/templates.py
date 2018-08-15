from jobwork.db_connection import db


class Templates(object):
    @classmethod
    def find(cls, *args, **kwargs):
        return db.templates.find(*args, **kwargs)

    @classmethod
    def find_one(cls, *args, **kwargs):
        return db.templates.find_one(*args, **kwargs)

    @classmethod
    def update(cls, *args, **kwargs):
        return db.templates.update(*args, **kwargs)

    @classmethod
    def insert(cls, *args, **kwargs):
        return db.templates.insert(*args, **kwargs)

    @classmethod
    def count(cls, *args, **kwargs):
        return db.templates.count(*args, **kwargs)
    @classmethod
    def aggregate(cls,*args,**kwargs):
        return db.templates.aggregate(*args, **kwargs)