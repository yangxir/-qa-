from flask import Blueprint, render_template, jsonify, redirect, url_for, session
from exts import mail, db
from flask_mail import Message
from flask import request
import random
from models import EmailCaptchaModel, UserModel
from .forms import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash


# /auth
bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        form = LoginForm(request.form)
        if form.validate():
            return redirect('/')
        else:
            print(form.errors)
            return redirect(url_for('auth.login'))


# GET: 从服务器获取数据
# POST:将客户端数据提交给服务器
@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        # 验证用户提交的邮箱和邮箱验证码是否一致
        # 表单验证: flask-wtf: wtforms
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            user = UserModel(email=email, username=username, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.login'))
        else:
            print(form.errors)
            return redirect(url_for('auth.register'))

# 没有指定方法，默认GET
@bp.route('/captcha/email', methods=['GET'])
def get_email_captcha():
    email = request.args.get('email')
    # 随机数字组合
    captcha = random.randint(1000, 9999)
    message = Message(subject='注册验证码', recipients=[email], body=f'您的验证码是{captcha}')
    mail.send(message)
    # memcached 存储在内存里，断电就无了
    # redis 数据类型更强大，同步机制（硬盘）
    # 这里用数据库存储，开销大
    email_already_in = EmailCaptchaModel.query.filter_by(email=email)
    # 如果之前发送过验证码，那么覆盖掉过去的，保留最新的
    if email_already_in.first():
        email_already_in.first().captcha = captcha
    # 之前没有发送过，直接加入数据库
    else:
        email_captcha = EmailCaptchaModel(email=email, captcha=captcha)
        db.session.add(email_captcha)
    db.session.commit()
    return jsonify({'code': 200, 'message': '', 'data': None})


@bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')
