from models.mongo import Mongo

class Answer(Mongo):
    __fields__ = Mongo.__fields__ + [
        ('q_id', int, ''),
        ('content', str, ''),
    ]