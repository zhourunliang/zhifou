from models.mongo import Mongo

class Question(Mongo):
    __fields__ = Mongo.__fields__ + [
        ('title', str, ''),
        ('content', str, ''),
        ('user', dict, {}),
        ('follows', dict, {}),
    ]

    def answers(self):
        from .answer import Answer
        ans = Answer.find_all(qid=self.id)
        return ans