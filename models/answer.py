from models.mongo import Mongo

class Answer(Mongo):
    __fields__ = Mongo.__fields__ + [
        ('qid', int, ''),
        ('uid', int, ''),
        ('content', str, ''),
    ]