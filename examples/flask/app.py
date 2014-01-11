#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2013, 2014 Mark Lee
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
'''
Example Flask app using pyoath-toolkit.
Only tested on Python 2.7.
'''

from flask import Flask, make_response, redirect, render_template, url_for
from flask.ext.login import (
    current_user, LoginManager, login_required, login_user, UserMixin)
from flask.ext.script import Manager
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.wtf import Form
from io import BytesIO
from oath_toolkit import qrcode
from oath_toolkit.wtforms import TOTPValidator
from random import SystemRandom
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.event import listens_for
from wtforms import PasswordField, TextField, ValidationError, validators
from wtforms.ext.sqlalchemy.orm import model_form

OTP_DIGITS = 6

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'Secret key example'
login_manager = LoginManager()
login_manager.init_app(app)
manager = Manager(app)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'

rand = SystemRandom()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    # The password is plaintext because this is an EXAMPLE.
    # DO NOT TRY THIS AT HOME.
    password = db.Column(db.String(255), nullable=False)

    oath_secret = db.Column(db.BINARY(255), nullable=False)

    def get_id(self):
        return unicode(self.id)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@listens_for(User, 'before_insert')
def generate_oath_secret(mapper, connection, target):
    target.oath_secret = b''.join([chr(rand.randint(0, 255))
                                   for _ in range(rand.randint(40, 80))])

RegisterForm = model_form(User, base_class=Form, exclude=['oath_secret'])


class LoginForm(Form):
    username = TextField(u'Username', [validators.required()])
    password = PasswordField(u'Password', [validators.required()])
    otp = PasswordField(u'One-time password')

    def validate(self):
        super(LoginForm, self).validate()
        try:
            self.user = db.session.query(User) \
                                  .filter_by(username=self.username.data,
                                             password=self.password.data) \
                                  .one()
        except InvalidRequestError:
            raise ValidationError(u'Could not find user.')
        TOTPValidator(OTP_DIGITS, 1, True)(self, self.otp)
        return True


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=('GET', 'POST'))
def register():
    context = {
        'registered': False,
    }
    form = RegisterForm()
    if form.validate_on_submit():
        user = User()
        form.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        context['registered'] = True
        context['user'] = user
        login_user(user)
    else:
        context['form'] = form
    return render_template('register.html', **context)


@app.route('/register/qrcode', methods=('GET',))
def oath_qrcode():
    img = qrcode.generate('totp', current_user.oath_secret,
                          current_user.username, 'Test App',
                          border=2, box_size=4)[1]
    stream = BytesIO()
    img.save(stream, 'PNG')
    resp = make_response(stream.getvalue(), 200)
    resp.headers['Content-Type'] = 'image/png'
    return resp


@app.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        login_user(form.user)
        print('Done!')
        return redirect(url_for('protected'))
    return render_template('login.html', form=form)


@app.route('/protected')
@login_required
def protected():
    return render_template('protected.html')

if __name__ == '__main__':
    manager.run()
