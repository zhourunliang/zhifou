from models.mongo import Mongo
from utils import log

class User(Mongo):
    __fields__ = Mongo.__fields__ + [
        ('username', str, ''),
        ('password', str, ''),
        ('user_image', str, ''),
    ]

    """
        User 是一个保存用户数据的 model
        现在只有两个属性 username 和 password
        """

    def __init__(self):
        self.user_image = 'default.png'

    def salted_password(self, password, salt='$!@><?>HUI&DWQa`'):
        import hashlib
        def sha256(ascii_str):
            return hashlib.sha256(ascii_str.encode('ascii')).hexdigest()

        hash1 = sha256(password)
        hash2 = sha256(hash1 + salt)
        return hash2

    def hashed_password(self, pwd):
        import hashlib
        # 用 ascii 编码转换成 bytes 对象
        p = pwd.encode('ascii')
        s = hashlib.sha256(p)
        # 返回摘要字符串
        return s.hexdigest()

    @classmethod
    def register(cls, form):
        name = form.get('username', '')
        pwd = form.get('password', '')
        if len(name) < 2:
            return {'data': None, 'msg': '用户名不能少于2位', 'status': False} 
        elif not User.find_by(username=name) is None:
            return {'data': None, 'msg': '用户名已存在', 'status': False} 
        else:
            u = User.new(form)
            u.password = u.salted_password(pwd)
            u.save()
            return {'data': u, 'msg': '注册成功', 'status': True} 

    @classmethod
    def validate_login(cls, form):
        u = User()
        u.username = form.get("username", '')
        u.password = form.get("password", "")
        user = User.find_by(username=u.username)
        log('validate_login, user',user)
        if user is None:
            return {'data': None, 'msg': '用户名不存在', 'status': False} 
        elif user.password != u.salted_password(u.password):    
            return {'data': None, 'msg': '密码不正确', 'status': False} 
        else:
            return {'data': user, 'msg': '登陆成功', 'status': True} 