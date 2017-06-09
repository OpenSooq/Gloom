import hmac
import urlparse
import time

from pymongo import MongoClient, ReturnDocument, ASCENDING
from pymongo.errors import DuplicateKeyError

from .common import safe_base64, app_config

mongo = MongoClient(app_config.opt_string("mongo", "connection"))
db_name = app_config.opt_string("mongo", "database")
collection_name = app_config.opt_string("mongo", "collection")
db = mongo[db_name]
collection = db[collection_name]

class UrlShorten(object):
    def __init__(self, code=None, url=None, **kw):
        self.code = code
        self.url = self.validate_url(url)
        self.created_at = time.time()
        for key, value in kw.items():
            setattr(self, key, value)

    @property
    def short(self):
        return app_config.base_url+self.code

    @staticmethod
    def validate_url(value):
        ret = value
        parsed = urlparse.urlparse(value)
        if not parsed.netloc:
            ret = '//'+ret
        if not parsed.scheme:
            ret = 'http:'+ret
        return ret

    @classmethod
    def generate(cls, url, length):
        digest = hmac.HMAC(key=app_config.secret, msg=url).digest()
        code = safe_base64(digest)[:app_config.opt_int('main', 'code-length', length)]
        item = UrlShorten(code=code, url=url)
        return item

    @classmethod
    def generate_and_save(cls, url):
        for i in range(4, 16):
            item = cls.generate(url, i)
            saved = item.save()
            if saved:
                return item
            else:
                collesion = collection.find_one({"code":item.code})
                if collesion['url'] == item.url:
                    return cls(**collesion)
        return None

    def save(self):
        try:
            collection.insert_one({
                "code": self.code,
                "url": self.url,
                "created_at": self.created_at,
                "clicks":0,
            })
        except DuplicateKeyError:
            return False
        return True

    @classmethod
    def find_by_code(cls, code):
        item = collection.find_one({"code":code})
        if not item: return None
        return cls(**item)


    @classmethod
    def find_and_increment(cls, code):
        item = collection.find_one_and_update(
            {"code":code},
            {'$inc': {'clicks': 1}, "$set": {"updated_at":time.time()}},
            upsert=False,
            return_document=ReturnDocument.AFTER
        )
        if not item: return None
        return cls(**item)


def migrate():
    collection.ensure_index([('code', ASCENDING)], unique=True)
