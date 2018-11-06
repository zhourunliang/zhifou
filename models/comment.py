from models.mongo import Mongo

class Comment(Mongo):
    __fields__ = Mongo.__fields__ + [
        ('a_id', int, ''),
        ('content', str, ''),
    ]