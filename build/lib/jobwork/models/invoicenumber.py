from jobwork.db_connection import db


class InvoiceNumbers(object):
    @classmethod
    def find(cls, *args, **kwargs):
        return db.invoicenumbers.find(*args, **kwargs)

    @classmethod
    def find_one(cls, *args, **kwargs):
        return db.invoicenumbers.find_one(*args, **kwargs)

    @classmethod
    def update(cls, *args, **kwargs):
        return db.invoicenumbers.update(*args, **kwargs)

    @classmethod
    def insert(cls, *args, **kwargs):
        return db.invoicenumbers.insert(*args, **kwargs)

    @classmethod
    def count(cls, *args, **kwargs):
        return db.invoicenumbers.count(*args, **kwargs)
