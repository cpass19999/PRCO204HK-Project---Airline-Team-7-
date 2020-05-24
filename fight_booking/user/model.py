from sqlalchemy import PrimaryKeyConstraint, text
from fight_booking import db, bcrypt
from itsdangerous import TimedJSONWebSignatureSerializer
from itsdangerous import SignatureExpired, BadSignature
from flask import current_app, flash
from flask_login import UserMixin
from fight_booking import login
from datetime import datetime

##  設置中繼的關聯表
#  flask-sqlalchemy會自動的在資料庫中產生相對應的table
relations_user_role = db.Table('relation_user_role',
                               db.Column('user_id', db.Integer, db.ForeignKey('tbl_user.user_id')),
                               db.Column('role_id', db.Integer, db.ForeignKey('roles.id')))

#  在relation_user_role的下方加入
#  設置Role與Func中繼關聯表
relations_role_func = db.Table('relations_role_func',
                               db.Column('func_id', db.Integer, db.ForeignKey('funcs.id')),
                               db.Column('role_id', db.Integer, db.ForeignKey('roles.id')))


class UserReister(UserMixin, db.Model):
    """記錄使用者資料的資料表"""
    __tablename__ = 'tbl_user'
    __table_args__ = (
        PrimaryKeyConstraint('user_id'),
    )
    user_id = db.Column(db.Integer, autoincrement=True, primark_key=True)
    user_username = db.Column(db.String(80), unique=True, nullable=False)
    user_email = db.Column(db.String(80), unique=True, nullable=False)
    # user_password = db.Column(db.String(50), nullable=False)
    user_confirm = db.Column(db.Boolean, default=False)
    password_hash = db.Column(db.String(150), nullable=False)
    user_fullname = db.Column(db.String(50))
    passportID = db.Column(db.String(20))
    passport_expiration = db.Column(db.DateTime)
    passport_country = db.Column(db.String(20))
    contactNo = db.Column(db.Integer)
    # about_me = db.Column(db.Text())

    gender = db.Column(db.Text)
    address = db.Column(db.String(20))
    regist_date = db.Column(db.DateTime, default=datetime.utcnow())
    last_login = db.Column(db.DateTime, default=datetime.utcnow())

    # flights = db.relationship("Flight", secondary="booking"  , backref=db.backref('users', lazy=True) )
    orders = db.relationship("Order", backref=db.backref('users', lazy=True))

    roles = db.relationship('Role', secondary=relations_user_role, lazy='subquery', backref=db.backref('users', lazy=True))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf8')

    def check_password(self, password):
        """
        密碼驗證，驗證使用者輸入的密碼跟資料庫內的加密密碼是否相符
        :param password: 使用者輸入的密碼
        :return: True/False
        """
        return bcrypt.check_password_hash(self.password_hash, password)

    def create_confirm_token(self, expires_in=3600):
        """
        利用itsdangerous來生成令牌，透過current_app來取得目前flask參數['SECRET_KEY']的值
        :param expiration: 有效時間，單位為秒
        :return: 回傳令牌，參數為該註冊用戶的id
        """
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'], expires_in=expires_in)
        return s.dumps({'user_id': self.user_id})

    def validate_confirm_token(self, token):
        """
        驗證回傳令牌是否正確，若正確則回傳True
        :param token:驗證令牌
        :return:回傳驗證是否正確，正確為True
        """
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)  # 驗證
        except SignatureExpired:
            #  當時間超過的時候就會引發SignatureExpired錯誤
            return False
        except BadSignature:
            #  當驗證錯誤的時候就會引發BadSignature錯誤
            return False
        return data

    def get_id(self):
        return self.user_id

    def create_reset_token(self, expires_in=3600):
        """
        提供申請遺失密碼認證使用的token
        :param expires_in: 有效時間(秒)
        :return:token
        """
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'], expires_in=expires_in)
        return s.dumps({'reset_id': self.id})

    def check_admin(self, func_module, func_name):
        """
        檢查使用者是否有權限進入該View Function
        :param
            func_module: View Function的module
            func_name: View Function的name
        :return:
            result: 有無權限 boolean
        """
        #  取得個人的權限表
        func_list = self.user_func
        #  func的table中記錄是module+.+func_name
        view_function = func_module + '.' + func_name
        result = func_list.filter(text("func_module_name=:view_function")).params(view_function=view_function).first()
        if result:
            #flash(view_function)
            return True
        else:
            #flash(view_function)
            return False

    def has_role(self,role_name):
        role_list = self.user_role
        result = role_list.filter(text("name=:role_name")).params(role_name=role_name).first()
        if result:
            return True
        else:
            return False

    def __repr__(self):
        return 'user_username:%s, user_email:%s' % (self.user_username, self.user_email)

    @property
    def user_role(self):
        role_list = Role.query.join(relations_user_role)\
                .join(UserReister)\
                .filter(UserReister.user_id == self.user_id)
        return role_list


    @property
    def user_func(self):
        func_list = Func.query.join(relations_role_func) \
            .join(Role) \
            .join(relations_user_role) \
            .join(UserReister) \
            .filter(UserReister.user_id == self.user_id)
        return func_list


@login.user_loader
def load_user(user_id):
    return UserReister.query.get(int(user_id))


class Role(db.Model):
    """
    權限角色主表
    不需設置ForeignKey，會透過SQLAlehemy的多對多關聯機制處理
    :parameter
        name:角色名稱
    """
    __tablename__ = 'roles'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    funcs = db.relationship('Func', secondary=relations_role_func, lazy='subquery',
                            backref=db.backref('roles', lazy=True))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name




class Func(db.Model):
    """
    :description
        專案中的View Function主表
        不需設置ForeignKey，會透過SQLAlchemy的多對多關聯機制處理

    :parameter
        func_module_name: View Function module+name
        func_description: View Function功能說明
        func_is_activate: View Function是否啟動
            default: True
        func_remark: View Function備註

    """
    __tablename__ = 'funcs'
    id = db.Column(db.Integer, primary_key=True)
    func_module_name = db.Column(db.String(50))
    func_description = db.Column(db.String(100))
    func_is_activate = db.Column(db.Boolean, default=True)
    func_remark = db.Column(db.String(100))

    def __init__(self, func_module_name, func_description, func_is_activate=True, func_remark=None):
        self.func_module_name = func_module_name
        self.func_description = func_description
        self.func_is_activate = func_is_activate
        self.func_remark = func_remark

    def __repr__(self):
        return 'id = %i, module_name = %s, is_activate = %s'

# db.create_all()
