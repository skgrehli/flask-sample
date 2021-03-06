from jobwork.db_connection import db


class JobReviews(object):
    @classmethod
    def find(cls, *args, **kwargs):
        return db.jobreviews.find(*args, **kwargs)

    @classmethod
    def find_one(cls, *args, **kwargs):
        return db.jobreviews.find_one(*args, **kwargs)

    @classmethod
    def update(cls, *args, **kwargs):
        return db.jobreviews.update(*args, **kwargs)

    @classmethod
    def insert(cls, *args, **kwargs):
        return db.jobreviews.insert(*args, **kwargs)

    @classmethod
    def count(cls, *args, **kwargs):
        return db.jobreviews.count(*args, **kwargs)
