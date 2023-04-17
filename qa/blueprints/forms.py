import wtforms
from wtforms.validators import Email, Length, EqualTo, InputRequired
from models import UserModel, EmailCaptchaModel
from exts import db
from werkzeug.security import check_password_hash
from flask import session


class RegisterForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message='邮箱格式错误!')])
    captcha = wtforms.StringField(validators=[Length(min=4, max=4, message='验证码格式错误！')])
    username = wtforms.StringField(validators=[Length(min=3, max=20, message='用户名格式错误！')])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message='密码格式错误！')])
    password_confirm = wtforms.StringField(validators=[EqualTo('password')])

    # 自定义验证
    # 1. 邮箱是否被注册
    # 2. 验证码是否正确
    def validate_email(self, field):
        email = field.data
        user = UserModel.query.filter_by(email=email).first()
        if user:
            raise wtforms.ValidationError(message='该邮箱已经被注册！')

    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        captcha_model = EmailCaptchaModel.query.filter_by(email=email, captcha=captcha).first()
        if not captcha_model:
            raise wtforms.ValidationError(message='邮箱或验证码错误！')
        # 删除验证码
        else:
            db.session.delete(captcha_model)
            db.session.commit()


class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message='邮箱格式错误!')])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message='密码格式错误！')])

    # 自定义验证
    # 邮箱是否注册
    def validate_email(self, field):
        email = field.data
        password = self.password.data
        user = UserModel.query.filter_by(email=email).first()
        # 没有此用户
        if not user:
            raise wtforms.ValidationError(message='该邮箱未注册！')
        else:
            # 账号密码正确
            if check_password_hash(user.password, password):
                # cookie:
                # 使用cookie存储登录授权
                # flask中的session经过加密存储在cookie中
                session['user_id'] = user.id
            # 账号密码错误
            else:
                raise wtforms.ValidationError(message='账号密码错误！')


class QuestionForm(wtforms.Form):
    title = wtforms.StringField(validators=[Length(min=3, max=100, message='邮箱格式错误!')])
    content = wtforms.StringField(validators=[Length(min=3, message='验证码格式错误！')])


class AnswerForm(wtforms.Form):
    content = wtforms.StringField(validators=[Length(min=1, message='回答最短需要1个字！')])
    question_id = wtforms.IntegerField(validators=[InputRequired(message='必须传入问题Id！')])

