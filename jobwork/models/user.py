from jobwork.db_connection import db


# noinspection SpellCheckingInspection
class User(object):
    @classmethod
    def find(cls, *args, **kwargs):
        return db.user.find(*args, **kwargs)

    @classmethod
    def find_one(cls, *args, **kwargs):
        return db.user.find_one(*args, **kwargs)

    @classmethod
    def update(cls, *args, **kwargs):
        return db.user.update(*args, **kwargs)

    @classmethod
    def insert(cls, *args, **kwargs):
        return db.user.insert(*args, **kwargs)

    @classmethod
    def count(cls, *args, **kwargs):
        return db.user.count(*args, **kwargs)


    @classmethod
    def find_FCM_id(cls, userid):
        try:
            result = cls.find_one({"userid": int(userid)})
            if "device_token" in result:
                return result['device_token']
            else:
                return False
        except Exception as e:
            raise e
