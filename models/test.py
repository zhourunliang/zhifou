from models.mongo import Mongo

class Test(Mongo):
    __fields__ = Mongo.__fields__ + [
        ('title', str, ''),
    ]