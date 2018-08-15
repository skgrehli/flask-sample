import hashlib
import linecache
import random
import uuid

import sys

from jobwork.models.user import User


class CommonUtils(object):
    @classmethod
    def generateRandomName(cls):
        alpha = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_"
        name = ''.join(random.choice(alpha) for i in range(random.randint(25, 30)))
        name = (hashlib.sha384(name)).hexdigest()
        return name

    @classmethod
    def generateRandomNo(cls, database, key):
        number = random.randint(100000000, 999999999)
        result = database.find_one({key: number})
        if result is None:
            return number
        else:
            cls.generateRandomNo(database, key)

    @classmethod
    def getHash(cls, hash_len):
        # ascii_uppercase
        alpha = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        hash = ''.join(random.choice(alpha) for i in range(hash_len))
        return hash

    @classmethod
    def getHashValue(cls):
        randomvalue = (hashlib.sha512(uuid.uuid4().hex.encode())).hexdigest() + (
            hashlib.sha512(uuid.uuid4().hex.encode())).hexdigest()
        # randomvalue = hash_object.hexdigest()
        return randomvalue

    @classmethod
    def generateOTP(cls):
        userotp = str(random.randrange(100000, 1000000))
        return userotp

    @classmethod
    def password_hash(cls, password, salt):
        return hashlib.md5(password.strip()).hexdigest() + salt

    @classmethod
    def print_exception(cls):
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))
