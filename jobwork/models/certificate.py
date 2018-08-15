from jobwork.db_connection import db


class Certificate(object):
    @classmethod
    def find(cls, *args, **kwargs):
        return db.certificate.find(*args, **kwargs)

    @classmethod
    def find_one(cls, *args, **kwargs):
        return db.certificate.find_one(*args, **kwargs)

    @classmethod
    def update(cls, *args, **kwargs):
        return db.certificate.update(*args, **kwargs)

    @classmethod
    def insert(cls, *args, **kwargs):
        return db.certificate.insert(*args, **kwargs)

    @classmethod
    def count(cls, *args, **kwargs):
        return db.certificate.count(*args, **kwargs)
