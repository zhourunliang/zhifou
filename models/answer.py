from models.mongo import Mongo

class Answer(Mongo):
    __fields__ = Mongo.__fields__ + [
        ('qid', int, ''),
        ('content', str, ''),
        ('user', dict, {}),
    ]

    def question(self):
        from .question import Question
        qu = Question.get(self.qid)
        return qu