from models.mongo import Mongo

class Answer(Mongo):
    __fields__ = Mongo.__fields__ + [
        ('qid', int, 0),
        ('content', str, ''),
        ('uid', int, 0),
        ('user', dict, {}),
        ('like', int, 0),
        ('unlike', int, 0),
    ]

    def question(self):
        from .question import Question
        qu = Question.get(self.qid)
        return qu